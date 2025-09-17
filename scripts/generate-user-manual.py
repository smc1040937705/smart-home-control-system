#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能家居控制系统用户手册生成脚本
- 从模板文件生成用户手册
- 验证手册格式和内容
- 支持错误检测和报告
"""

import os
import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class UserManualGenerator:
    def __init__(self, template_path: str, output_path: str):
        self.template_path = template_path
        self.output_path = output_path
        self.required_sections = [
            "overview", "device-setup", "feature-guide", 
            "troubleshooting", "safety-guidelines"
        ]
    
    def load_template(self) -> str:
        """加载模板文件"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"模板文件不存在: {self.template_path}")
        except Exception as e:
            raise Exception(f"加载模板文件失败: {str(e)}")
    
    def validate_template(self, content: str) -> Dict[str, bool]:
        """验证模板内容"""
        validation_results = {}
        
        # 检查必需章节
        for section in self.required_sections:
            section_pattern = rf"##\s+{section.replace('-', r'[\s-]*')}\s*\([^)]+\)"
            validation_results[f"section_{section}"] = bool(re.search(section_pattern, content, re.IGNORECASE))
        
        # 检查基本格式
        validation_results["has_title"] = bool(re.search(r"^#\s+.+", content, re.MULTILINE))
        validation_results["has_overview"] = "overview" in content.lower()
        validation_results["has_safety"] = "safety" in content.lower()
        
        return validation_results
    
    def generate_manual(self, custom_data: Optional[Dict] = None) -> str:
        """生成用户手册"""
        template_content = self.load_template()
        
        # 验证模板
        validation = self.validate_template(template_content)
        if not all(validation.values(