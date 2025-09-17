#!/usr/bin/env python3
"""
Smart Home Control System - User Manual Generator

This script generates user manuals from templates with validation and formatting.
"""

import os
import sys
import re
import argparse
import datetime
from pathlib import Path
from typing import Dict, List, Tuple

class UserManualGenerator:
    def __init__(self):
        self.required_sections = [
            "Overview",
            "Device Setup", 
            "Feature Guide",
            "Troubleshooting",
            "Safety Guidelines"
        ]
        
        self.validation_errors = []
        self.validation_warnings = []
    
    def load_template(self, template_path: str) -> str:
        """Load the user manual template file."""
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            self.validation_errors.append(f"Template file not found: {template_path}")
            return ""
        except Exception as e:
            self.validation_errors.append(f"Error reading template: {str(e)}")
            return ""
    
    def validate_template_structure(self, content: str) -> bool:
        """Validate that the template contains all required sections."""
        valid = True
        
        for section in self.required_sections:
            # Look for section headers (## followed by section name)
            pattern = rf'^##\s+{re.escape(section)}\s*$'
            if not re.search(pattern, content, re.MULTILINE):
                self.validation_errors.append(f"Missing required section: {section}")
                valid = False
        
        return valid
    
    def validate_content_quality(self, content: str) -> bool:
        """Perform basic content quality checks."""
        valid = True
        
        # Check for placeholder content
        placeholders = ["{{.*?}}", "\[.*?\]", "TODO", "FIXME"]
        for placeholder in placeholders:
            matches = re.findall(placeholder, content)
            if matches:
                self.validation_warnings.append(f"Found placeholder content: {matches[:3]}")
        
        # Check minimum content length
        if len(content.strip()) < 1000:
            self.validation_warnings.append("Template content seems very short")
        
        return valid
    
    def generate_manual(self, template_content: str, output_path: str, **replacements) -> bool:
        """Generate the final user manual with replacements."""
        try:
            # Apply replacements
            manual_content = template_content
            for key, value in replacements.items():
                manual_content = manual_content.replace(f"{{{{{key}}}}}", str(value))
            
            # Ensure output directory exists
            output_dir = os.path.dirname(output_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            
            # Write the generated manual
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(manual_content)
            
            print(f"✓ User manual generated: {output_path}")
            return True
            
        except Exception as e:
            self.validation_errors.append(f"Error generating manual: {str(e)}")
            return False
    
    def run_validation_report(self) -> bool:
        """Generate a validation report."""
        if self.validation_errors:
            print("\n❌ VALIDATION ERRORS:")
            for error in self.validation_errors:
                print(f"  - {error}")
        
        if self.validation_warnings:
            print("\n⚠️  VALIDATION WARNINGS:")
            for warning in self.validation_warnings:
                print(f"  - {warning}")
        
        return len(self.validation_errors) == 0
    
    def generate_validation_summary(self) -> Dict:
        """Generate a summary of validation results."""
        return {
            "errors": self.validation_errors,
            "warnings": self.validation_warnings,
            "is_valid": len(self.validation_errors) == 0,
            "required_sections_present": all(
                section in self.required_sections for section in self.required_sections
            )
        }

def main():
    parser = argparse.ArgumentParser(description='Generate user manual from template')
    parser.add_argument('--template', '-t', default='docs/user-manual-template.md', 
                       help='Path to template file')
    parser.add_argument('--output', '-o', default='docs/user-manual.md',
                       help='Output path for generated manual')
    parser.add_argument('--validate-only', '-v', action='store_true',
                       help='Only validate template without generating output')
    parser.add_argument('--system-version', default='2.0.0',
                       help='System version to include in manual')
    
    args = parser.parse_args()
    
    generator = UserManualGenerator()
    
    # Load and validate template
    template_content = generator.load_template(args.template)
    
    if not template_content:
        print("❌ Failed to load template")
        generator.run_validation_report()
        sys.exit(1)
    
    # Validate template structure
    structure_valid = generator.validate_template_structure(template_content)
    content_valid = generator.validate_content_quality(template_content)
    
    if args.validate_only:
        generator.run_validation_report()
        sys.exit(0 if structure_valid and content_valid else 1)
    
    # Generate manual with replacements
    replacements = {
        'CURRENT_DATE': datetime.datetime.now().strftime('%Y-%m-%d'),
        'SYSTEM_VERSION': args.system_version
    }
    
    success = generator.generate_manual(template_content, args.output, **replacements)
    
    # Run validation report
    generator.run_validation_report()
    
    if success and structure_valid and content_valid:
        print("\n✅ User manual generation completed successfully!")
        
        # Generate validation summary for CI/CD
        summary = generator.generate_validation_summary()
        print(f"\n📊 Validation Summary:")
        print(f"  - Errors: {len(summary['errors'])}")
        print(f"  - Warnings: {len(summary['warnings'])}")
        print(f"  - Required Sections: {len(summary['required_sections_present'])}/{len(generator.required_sections)}")
        
        sys.exit(0)
    else:
        print("\n❌ User manual generation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()