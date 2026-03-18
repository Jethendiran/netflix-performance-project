import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

def load_locust_results():
    """Load all Locust CSV results"""
    stats_files = glob.glob("*_stats.csv")
    if not stats_files:
        print("❌ No stats files found. Run load tests first.")
        return None
    
    results = {}
    for file in stats_files:
        test_name = file.replace('_stats.csv', '')
        results[test_name] = pd.read_csv(file)
        print(f"✅ Loaded: {file}")
    
    return results

def create_comparison_charts(results):
    """Create before/after comparison graphs"""
    
    if not results:
        return
    
    # Prepare data for comparison
    test_names = []
    p95_values = []
    throughput_values = []
    
    for name, df in results.items():
        test_names.append(name)
        p95_values.append(df['95%'].iloc[-1] if '95%' in df.columns else 0)
        throughput_values.append(df['Requests/s'].iloc[-1] if 'Requests/s' in df.columns else 0)
    
    # 1. Response Time Comparison (p95)
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    colors = ['red' if 'baseline' in name.lower() else 'green' for name in test_names]
    bars = plt.bar(test_names, p95_values, color=colors)
    plt.title('p95 Response Time Comparison', fontsize=14, fontweight='bold')
    plt.ylabel('Response Time (ms)')
    plt.xticks(rotation=45)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.0f}ms', ha='center', va='bottom')
    
    # 2. Throughput Comparison
    plt.subplot(1, 2, 2)
    bars = plt.bar(test_names, throughput_values, color=colors)
    plt.title('Throughput Comparison (Requests/sec)', fontsize=14, fontweight='bold')
    plt.ylabel('Requests per Second')
    plt.xticks(rotation=45)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f} req/s', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('performance_comparison.png', dpi=150, bbox_inches='tight')
    print("\n✅ Saved: performance_comparison.png")
    
    # 3. Create summary table
    summary_data = []
    for name, df in results.items():
        summary_data.append({
            'Test': name,
            'p50 (ms)': df['50%'].iloc[-1] if '50%' in df.columns else 0,
            'p95 (ms)': df['95%'].iloc[-1] if '95%' in df.columns else 0,
            'p99 (ms)': df['99%'].iloc[-1] if '99%' in df.columns else 0,
            'Throughput': df['Requests/s'].iloc[-1] if 'Requests/s' in df.columns else 0,
            'Error %': df['Error %'].iloc[-1] if 'Error %' in df.columns else 0
        })
    
    summary_df = pd.DataFrame(summary_data)
    print("\n📊 PERFORMANCE SUMMARY")
    print("="*70)
    print(summary_df.to_string(index=False))
    summary_df.to_csv('performance_summary.csv', index=False)
    print("\n✅ Saved: performance_summary.csv")

if __name__ == "__main__":
    print("📈 Generating Performance Charts...")
    results = load_locust_results()
    if results:
        create_comparison_charts(results)
        print("\n✨ Charts ready for presentation!")