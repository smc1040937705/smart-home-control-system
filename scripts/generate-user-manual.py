#!/usr/bin/env python3
"""
Smart Home Control System - User Manual Generator

This script generates user manuals from templates with validation and formatting.
"""

import os
import sys
import json
import argparse
import datetime
import re
from pathlib import Path
from typing import Dict, List, Optional


def validate_template_structure(content: str) -> Dict[str, bool]:
    """Validate that the template contains all required sections."""
    required_sections = [
        "Overview",
        "Device Setup", 
        "Feature Guide",
        "Troubleshooting",
        "Safety Guidelines"
    ]
    
    validation_results = {}
    
    for section in required_sections:
        # Check for section headers (## Section Name)
        pattern = rf'^##\s+{re.escape(section)}\s*$'
        if re.search(pattern, content, re.MULTILINE):
            validation_results[section] = True
        else:
            validation_results[section] = False
    
    return validation_results


def validate_markdown_format(content: str) -> List[str]:
    """Validate Markdown formatting and return any issues found."""
    issues = []
    
    # Check for proper header structure
    lines = content.split('\n')
    header_levels = []
    
    for i, line in enumerate(lines, 1):
        # Check header consistency
        if line.startswith('#'):
            level = len(line.split(' ')[0])
            header_levels.append((level, i))
    
    # Check header hierarchy (should not skip levels)
    if header_levels:
        previous_level = header_levels[0][0]
        for level, line_num in header_levels[1:]:
            if level > previous_level + 1:
                issues.append(f"Header level jump from {previous_level} to {level} at line {line_num}")
            previous_level = level
    
    # Check for broken links
    link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    for match in re.finditer(link_pattern, content):
        link_text, link_url = match.groups()
        if not link_url.strip():
            issues.append(f"Empty link URL for '{link_text}'")
    
    return issues


def generate_user_manual(template_path: str, output_path: str, variables: Optional[Dict] = None) -> bool:
    """Generate user manual from template with variable substitution."""
    
    if variables is None:
        variables = {}
    
    # Set default variables
    default_vars = {
        'date': datetime.datetime.now().strftime('%Y-%m-%d'),
        'version': '1.0.0',
        'system_name': 'Smart Home Control System'
    }
    default_vars.update(variables)
    
    try:
        # Read template
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Validate template structure
        validation = validate_template_structure(template_content)
        missing_sections = [section for section, present in validation.items() if not present]
        
        if missing_sections:
            print(f"ERROR: Missing required sections: {', '.join(missing_sections)}")
            return False
        
        # Validate Markdown format
        format_issues = validate_markdown_format(template_content)
        if format_issues:
            print("WARNING: Format issues found:")
            for issue in format_issues:
                print(f"  - {issue}")
        
        # Perform variable substitution
        manual_content = template_content
        for key, value in default_vars.items():
            placeholder = f'{{{{{key}}}}}'
            manual_content = manual_content.replace(placeholder, str(value))
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Write generated manual
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(manual_content)
        
        print(f"✓ User manual generated successfully: {output_path}")
        print(f"✓ Template validation passed")
        
        if format_issues:
            print(f"⚠  {len(format_issues)} format warnings (manual will still be generated)")
        
        return True
        
    except FileNotFoundError:
        print(f"ERROR: Template file not found: {template_path}")
        return False
    except Exception as e:
        print(f"ERROR: Failed to generate manual: {e}")
        return False


def generate_validation_report(template_path: str, report_path: str) -> bool:
    """Generate a detailed validation report for the template."""
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Perform validations
        structure_validation = validate_template_structure(content)
        format_issues = validate_markdown_format(content)
        
        # Calculate statistics
        total_lines = len(content.split('\n'))
        word_count = len(content.split())
        section_count = sum(1 for line in content.split('\n') if line.startswith('## '))
        
        # Generate report
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'template_file': template_path,
            'validation': {
                'structure': structure_validation,
                'all_sections_present': all(structure_validation.values()),
                'format_issues': format_issues,
                'format_issues_count': len(format_issues)
            },
            'statistics': {
                'total_lines': total_lines,
                'word_count': word_count,
                'section_count': section_count,
                'file_size_bytes': len(content.encode('utf-8'))
            },
            'status': 'PASS' if all(structure_validation.values()) and not format_issues else 'WARNING'
        }
        
        # Ensure report directory exists
        report_dir = os.path.dirname(report_path)
        if report_dir:
            os.makedirs(report_dir, exist_ok=True)
        
        # Write JSON report
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Validation report generated: {report_path}")
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to generate validation report: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Generate user manuals from templates')
    parser.add_argument('--template', '-t', default='docs/templates/user-manual-template.md',
                       help='Path to template file')
    parser.add_argument('--output', '-o', default='docs/user-manual.md',
                       help='Output path for generated manual')
    parser.add_argument('--report', '-r', default='reports/validation-report.json',
                       help='Path for validation report')
    parser.add_argument('--version', '-v', help='System version number')
    parser.add_argument('--validate-only', action='store_true',
                       help='Only validate template without generating manual')
    
    args = parser.parse_args()
    
    # Prepare variables
    variables = {}
    if args.version:
        variables['version'] = args.version
    
    print("🔧 Smart Home Control System - User Manual Generator")
    print("=" * 60)
    
    if args.validate_only:
        # Only validate and generate report
        success = generate_validation_report(args.template, args.report)
        sys.exit(0 if success else 1)
    else:
        # Generate manual and report
        manual_success = generate_user_manual(args.template, args.output, variables)
        report_success = generate_validation_report(args.template, args.report)
        
        if manual_success and report_success:
            print("\n🎉 Generation completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Generation failed!")
            sys.exit(1)


if __name__ == "__main__":
    main()