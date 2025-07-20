#!/usr/bin/env python3
"""
Quick start example for thermal-scout CLI
"""

import subprocess
import sys


def run_example(cmd: str, description: str):
    """Run an example command and show output"""
    print(f"\n{'='*60}")
    print(f"Example: {description}")
    print(f"Command: {cmd}")
    print(f"{'='*60}\n")
    
    subprocess.run(cmd, shell=True)


def main():
    """Run thermal-scout examples"""
    print("🔍 Thermal Scout - Quick Start Examples\n")
    
    examples = [
        ("thermal-scout search 'sentiment analysis' --limit 5", 
         "Search for sentiment analysis models with thermal awareness"),
        
        ("thermal-scout analyze 'distilbert-base-uncased'",
         "Analyze a specific model's thermal footprint"),
        
        ("thermal-scout recommend 'text generation for creative writing' --max-thermal medium",
         "Get model recommendations for a specific task"),
        
        ("thermal-scout compare bert-base-uncased roberta-base distilbert-base-uncased",
         "Compare multiple models side-by-side"),
        
        ("thermal-scout cache info",
         "Check cache information"),
    ]
    
    for cmd, desc in examples:
        run_example(cmd, desc)
        input("\nPress Enter to continue to next example...")


if __name__ == "__main__":
    main()