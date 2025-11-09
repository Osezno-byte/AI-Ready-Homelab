#!/usr/bin/env python3
"""
CSE Policy Validator

Validates CSE (Claude Supervised Execute) policy YAML files for:
- Required keys and structure
- Valid regex patterns
- Safe TTL values
- Infrastructure categorization
- Approval workflow configuration

Usage:
    python cse_policy_validator.py <policy-file.yaml>

Exit codes:
    0 = Valid policy
    1 = Invalid policy (prints errors)
"""

import sys
import re
import yaml
from pathlib import Path


class CSEPolicyValidator:
    """Validates CSE policy YAML files"""

    REQUIRED_TOP_LEVEL = ['version', 'metadata', 'infrastructures', 'approval_workflow']
    REQUIRED_METADATA = ['name', 'description', 'owner', 'last_updated']
    REQUIRED_INFRA = ['enabled', 'ttl_minutes', 'requires_approval', 'allowed_commands']
    REQUIRED_APPROVAL = ['mode', 'timeout_seconds', 'notification_channels']

    MAX_TTL_MINUTES = 480  # 8 hours max session
    MIN_TTL_MINUTES = 5    # 5 minutes minimum
    MAX_TIMEOUT_SECONDS = 300  # 5 minutes max approval timeout

    VALID_APPROVAL_MODES = ['interactive', 'notify-only', 'auto-approve']
    VALID_INFRA_NAMES = ['homeassistant', 'pfsense', 'vms', 'proxmox']

    def __init__(self, policy_path: Path):
        self.policy_path = policy_path
        self.errors = []
        self.warnings = []
        self.policy = None

    def validate(self) -> bool:
        """Run all validations. Returns True if valid, False otherwise."""
        if not self._load_yaml():
            return False

        self._validate_structure()
        self._validate_metadata()
        self._validate_infrastructures()
        self._validate_approval_workflow()
        self._validate_regex_patterns()
        self._validate_security_constraints()

        return len(self.errors) == 0

    def _load_yaml(self) -> bool:
        """Load and parse YAML file"""
        try:
            with open(self.policy_path, 'r') as f:
                self.policy = yaml.safe_load(f)
            return True
        except FileNotFoundError:
            self.errors.append(f"File not found: {self.policy_path}")
            return False
        except yaml.YAMLError as e:
            self.errors.append(f"YAML parse error: {e}")
            return False

    def _validate_structure(self):
        """Validate top-level structure"""
        if not isinstance(self.policy, dict):
            self.errors.append("Policy must be a YAML dictionary")
            return

        for key in self.REQUIRED_TOP_LEVEL:
            if key not in self.policy:
                self.errors.append(f"Missing required top-level key: {key}")

    def _validate_metadata(self):
        """Validate metadata section"""
        if 'metadata' not in self.policy:
            return  # Already flagged in structure validation

        metadata = self.policy['metadata']
        if not isinstance(metadata, dict):
            self.errors.append("metadata must be a dictionary")
            return

        for key in self.REQUIRED_METADATA:
            if key not in metadata:
                self.errors.append(f"Missing metadata.{key}")

        # Validate version format
        version = self.policy.get('version')
        if version and not re.match(r'^\d+\.\d+$', str(version)):
            self.errors.append(f"Invalid version format: {version} (expected X.Y)")

    def _validate_infrastructures(self):
        """Validate infrastructure definitions"""
        if 'infrastructures' not in self.policy:
            return

        infras = self.policy['infrastructures']
        if not isinstance(infras, dict):
            self.errors.append("infrastructures must be a dictionary")
            return

        for name, config in infras.items():
            # Validate infrastructure name
            if name not in self.VALID_INFRA_NAMES:
                self.warnings.append(
                    f"Non-standard infrastructure name: {name} "
                    f"(expected one of {self.VALID_INFRA_NAMES})"
                )

            # Validate required keys
            for key in self.REQUIRED_INFRA:
                if key not in config:
                    self.errors.append(f"Missing infrastructures.{name}.{key}")

            # Validate TTL
            ttl = config.get('ttl_minutes')
            if ttl is not None:
                if not isinstance(ttl, int):
                    self.errors.append(f"infrastructures.{name}.ttl_minutes must be an integer")
                elif ttl < self.MIN_TTL_MINUTES:
                    self.errors.append(
                        f"infrastructures.{name}.ttl_minutes too low: {ttl} "
                        f"(minimum {self.MIN_TTL_MINUTES})"
                    )
                elif ttl > self.MAX_TTL_MINUTES:
                    self.errors.append(
                        f"infrastructures.{name}.ttl_minutes too high: {ttl} "
                        f"(maximum {self.MAX_TTL_MINUTES})"
                    )

            # Validate enabled flag
            enabled = config.get('enabled')
            if enabled is not None and not isinstance(enabled, bool):
                self.errors.append(f"infrastructures.{name}.enabled must be boolean")

            # Validate requires_approval flag
            requires_approval = config.get('requires_approval')
            if requires_approval is not None and not isinstance(requires_approval, bool):
                self.errors.append(f"infrastructures.{name}.requires_approval must be boolean")

            # Validate allowed_commands
            allowed_commands = config.get('allowed_commands')
            if allowed_commands is not None:
                if not isinstance(allowed_commands, list):
                    self.errors.append(f"infrastructures.{name}.allowed_commands must be a list")
                elif not allowed_commands:
                    self.warnings.append(f"infrastructures.{name}.allowed_commands is empty")

    def _validate_approval_workflow(self):
        """Validate approval workflow configuration"""
        if 'approval_workflow' not in self.policy:
            return

        workflow = self.policy['approval_workflow']
        if not isinstance(workflow, dict):
            self.errors.append("approval_workflow must be a dictionary")
            return

        for key in self.REQUIRED_APPROVAL:
            if key not in workflow:
                self.errors.append(f"Missing approval_workflow.{key}")

        # Validate mode
        mode = workflow.get('mode')
        if mode and mode not in self.VALID_APPROVAL_MODES:
            self.errors.append(
                f"Invalid approval_workflow.mode: {mode} "
                f"(expected one of {self.VALID_APPROVAL_MODES})"
            )

        # Validate timeout
        timeout = workflow.get('timeout_seconds')
        if timeout is not None:
            if not isinstance(timeout, int):
                self.errors.append("approval_workflow.timeout_seconds must be an integer")
            elif timeout > self.MAX_TIMEOUT_SECONDS:
                self.warnings.append(
                    f"approval_workflow.timeout_seconds is high: {timeout}s "
                    f"(recommended max {self.MAX_TIMEOUT_SECONDS}s)"
                )

        # Validate notification channels
        channels = workflow.get('notification_channels')
        if channels is not None:
            if not isinstance(channels, list):
                self.errors.append("approval_workflow.notification_channels must be a list")
            elif not channels:
                self.warnings.append("approval_workflow.notification_channels is empty")

    def _validate_regex_patterns(self):
        """Validate any regex patterns in allowed_commands"""
        if 'infrastructures' not in self.policy:
            return

        for name, config in self.policy['infrastructures'].items():
            allowed_commands = config.get('allowed_commands', [])
            if not isinstance(allowed_commands, list):
                continue

            for cmd in allowed_commands:
                if not isinstance(cmd, str):
                    continue

                # Check if command contains regex metacharacters
                if any(char in cmd for char in ['*', '+', '?', '[', ']', '(', ')', '{', '}']):
                    try:
                        re.compile(cmd)
                    except re.error as e:
                        self.errors.append(
                            f"Invalid regex in infrastructures.{name}.allowed_commands: "
                            f"'{cmd}' - {e}"
                        )

    def _validate_security_constraints(self):
        """Validate security-related constraints"""
        # Check for overly permissive patterns
        if 'infrastructures' not in self.policy:
            return

        for name, config in self.policy['infrastructures'].items():
            allowed_commands = config.get('allowed_commands', [])
            if not isinstance(allowed_commands, list):
                continue

            for cmd in allowed_commands:
                if not isinstance(cmd, str):
                    continue

                # Flag dangerous patterns
                if cmd.strip() == '*' or cmd.strip() == '.*':
                    self.warnings.append(
                        f"Overly permissive pattern in infrastructures.{name}.allowed_commands: "
                        f"'{cmd}' allows ALL commands"
                    )

                # Flag destructive commands without approval
                destructive_keywords = ['rm -rf', 'dd if=', 'mkfs', 'fdisk', 'parted']
                if any(keyword in cmd.lower() for keyword in destructive_keywords):
                    if not config.get('requires_approval', False):
                        self.warnings.append(
                            f"Potentially destructive command '{cmd}' in {name} "
                            f"without requires_approval flag"
                        )

    def print_results(self):
        """Print validation results"""
        if self.errors:
            print(f"\n❌ VALIDATION FAILED: {self.policy_path}")
            print(f"\n{len(self.errors)} error(s) found:\n")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")

        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} warning(s):\n")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")

        if not self.errors and not self.warnings:
            print(f"\n✅ VALID: {self.policy_path}")
            print("   All checks passed!")
        elif not self.errors:
            print(f"\n✅ VALID: {self.policy_path}")
            print("   Validation passed with warnings (review recommended)")


def main():
    if len(sys.argv) != 2:
        print("Usage: python cse_policy_validator.py <policy-file.yaml>")
        sys.exit(1)

    policy_path = Path(sys.argv[1])
    validator = CSEPolicyValidator(policy_path)

    is_valid = validator.validate()
    validator.print_results()

    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()
