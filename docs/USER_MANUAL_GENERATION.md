# User Manual Generation System

## Overview

This system provides automated generation of user manuals for the Smart Home Control System. It includes templates, generation scripts, and GitHub Actions workflows to ensure consistent and up-to-date documentation.

## Components

### 1. Template File
**Location**: `docs/templates/user-manual-template.md`

This template contains all required sections for a comprehensive user manual:
- **Overview**: System introduction and key features
- **Device Setup**: Installation and configuration instructions
- **Feature Guide**: Detailed functionality explanations
- **Troubleshooting**: Common issues and solutions
- **Safety Guidelines**: Important safety information

The template uses `{{variable}}` syntax for dynamic content replacement.

### 2. Generation Script
**Location**: `scripts/generate-user-manual.py`

#### Features:
- **Template Validation**: Ensures all required sections are present
- **Markdown Format Checking**: Validates proper formatting
- **Variable Substitution**: Replaces placeholders with actual values
- **Validation Reports**: Generates detailed JSON reports
- **Error Handling**: Comprehensive error detection and reporting

#### Usage:
```bash
# Generate manual with default settings
python scripts/generate-user-manual.py

# Generate with specific version
python scripts/generate-user-manual.py --version "2.1.0"

# Validate template only
python scripts/generate-user-manual.py --validate-only

# Custom output paths
python scripts/generate-user-manual.py --output docs/generated/manual.md --report reports/validation.json
```

### 3. GitHub Actions Workflow
**Location**: `.github/workflows/user-manual-generation.yml`

#### Triggers:
- Push to `main` or `develop` branches when template files change
- Pull requests targeting `main` branch
- Manual trigger via workflow dispatch

#### Jobs:
1. **generate-user-manual**: Generates manual and validation report
2. **validation-report**: Parses and displays validation results
3. **create-pr-comment**: Adds validation results as PR comments

#### Manual Trigger:
```yaml
workflow_dispatch:
  inputs:
    version:
      description: 'System version number'
      required: false
      default: '1.0.0'
```

## Validation Requirements

The system validates:

### Structural Validation
- All 5 required sections must be present
- Proper Markdown header hierarchy
- No skipped header levels

### Format Validation
- Valid Markdown syntax
- No broken links
- Consistent formatting

### Content Validation
- Variable placeholders are properly formatted
- No empty sections
- Logical content organization

## Output Files

### Generated Manual
**Default Location**: `docs/user-manual.md`

Contains the fully generated user manual with:
- All template content
- Variable substitutions
- Current date and version information

### Validation Report
**Default Location**: `reports/validation-report.json`

Includes:
- Validation status (PASS/WARNING)
- Section presence validation
- Format issues list
- Statistics (lines, words, file size)
- Timestamp information

## Customization

### Adding New Sections
1. Add section to template with `## Section Name` header
2. Update validation in `scripts/generate-user-manual.py`
3. Add to `required_sections` list in `validate_template_structure()`

### Adding New Variables
1. Add placeholder to template: `{{variable_name}}`
2. Update default variables in generation script
3. Add command-line argument if needed

### Modifying Workflow
1. Edit `.github/workflows/user-manual-generation.yml`
2. Add new validation steps as needed
3. Update artifact handling if output locations change

## Best Practices

1. **Keep Templates Updated**: Regularly review and update template content
2. **Test Changes**: Validate templates before committing
3. **Version Control**: Include version numbers in generated manuals
4. **Backup**: Keep previous versions of generated manuals
5. **Review**: Regularly review validation reports for improvements

## Troubleshooting

### Common Issues

**Template Validation Fails**:
- Check that all required sections are present
- Verify header formatting (## Section Name)

**Generation Script Errors**:
- Ensure Python 3.9+ is available
- Check file permissions

**Workflow Failures**:
- Review GitHub Actions logs
- Check file paths and permissions

### Debug Mode
Add `--verbose` flag to generation script for detailed output (future enhancement).

## Future Enhancements

- Multi-language support
- PDF generation
- Automated translation
- Enhanced formatting validation
- Integration with documentation hosting
- Version comparison and diff generation

---

*This documentation was automatically generated as part of the user manual generation system.*