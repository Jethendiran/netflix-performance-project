"""
MOCK TEST DATA GENERATOR
This creates sample test results so you can practice generating graphs
Even without the real API, you can see how your charts will look!
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import time

print("📊 Creating MOCK test data for practice...")
print("="*50)

# Create mock baseline data (before caching)
baseline_data = {
    'Timestamp': pd.date_range(start='2024-01-01 00:00:00', periods=180, freq='1s'),
    'Requests/s': np.random.normal(45, 5, 180),  # Average 45 req/s
    '50%': np.random.normal(120, 10, 180),       # p50 around 120ms
    '95%': np.random.normal(850, 50, 180),       # p95 around 850ms
    '99%': np.random.normal(2100, 100, 180),     # p99 around 2100ms
    'Error %': np.random.normal(2, 0.5, 180)      # 2% errors
}

# Create mock cache data (after caching)
cache_data = {
    'Timestamp': pd.date_range(start='2024-01-01 00:05:00', periods=300, freq='1s'),
    'Requests/s': np.random.normal(210, 15, 300),  # Average 210 req/s
    '50%': np.random.normal(25, 3, 300),           # p50 around 25ms
    '95%': np.random.normal(95, 8, 300),           # p95 around 95ms
    '99%': np.random.normal(210, 12, 300),         # p99 around 210ms
    'Error %': np.random.normal(0.1, 0.05, 300)     # 0.1% errors
}

# Save to CSV files
pd.DataFrame(baseline_data).to_csv('baseline_stats.csv', index=False)
pd.DataFrame(cache_data).to_csv('cache_stats.csv', index=False)

print("✅ Created mock baseline_stats.csv")
print("✅ Created mock cache_stats.csv")
print("\n📊 Mock Data Statistics:")
print("-"*30)
print(f"Baseline - Avg Throughput: 45 req/s, p95: 850ms")
print(f"With Cache - Avg Throughput: 210 req/s, p95: 95ms")
print(f"\n🎯 Improvement: {(210-45)/45*100:.1f}% throughput increase")
print(f"🎯 Improvement: {(850-95)/850*100:.1f}% p95 latency reduction")

# Create comparison graph
plt.figure(figsize=(15, 10))

# Subplot 1: Throughput Comparison
plt.subplot(2, 2, 1)
tests = ['Baseline', 'With Cache']
throughput = [45, 210]
colors = ['red', 'green']
bars = plt.bar(tests, throughput, color=colors)
plt.title('Throughput Comparison (Requests/sec)', fontsize=14, fontweight='bold')
plt.ylabel('Requests per Second')
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height} req/s', ha='center', va='bottom')

# Subplot 2: Latency Comparison
plt.subplot(2, 2, 2)
x = range(3)
baseline_latency = [120, 850, 2100]
cache_latency = [25, 95, 210]
plt.plot(['p50', 'p95', 'p99'], baseline_latency, marker='o', label='Baseline', color='red', linewidth=2)
plt.plot(['p50', 'p95', 'p99'], cache_latency, marker='s', label='With Cache', color='green', linewidth=2)
plt.title('Latency Comparison (ms)', fontsize=14, fontweight='bold')
plt.ylabel('Response Time (ms)')
plt.legend()
plt.grid(True, alpha=0.3)

# Subplot 3: Error Rate
plt.subplot(2, 2, 3)
error_baseline = 2.0
error_cache = 0.1
bars = plt.bar(['Baseline', 'With Cache'], [error_baseline, error_cache], color=['red', 'green'])
plt.title('Error Rate Comparison (%)', fontsize=14, fontweight='bold')
plt.ylabel('Error Percentage')
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height}%', ha='center', va='bottom')

# Subplot 4: Cache Hit Ratio
plt.subplot(2, 2, 4)
hit_ratio = 78
plt.pie([hit_ratio, 100-hit_ratio], labels=[f'Hits {hit_ratio}%', f'Misses {100-hit_ratio}%'], 
        colors=['green', 'lightgray'], autopct='%1.1f%%', startangle=90)
plt.title('Cache Hit Ratio', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('mock_performance_comparison.png', dpi=150)
print("\n✅ Created mock_performance_comparison.png")
print("   (You can use this to practice your presentation!)")

# Create summary table
summary = pd.DataFrame({
    'Metric': ['Throughput (req/s)', 'p50 (ms)', 'p95 (ms)', 'p99 (ms)', 'Error Rate (%)', 'Cache Hit Ratio (%)'],
    'Baseline': ['45', '120', '850', '2100', '2.0', '0'],
    'With Cache': ['210', '25', '95', '210', '0.1', '78'],
    'Improvement': ['+367%', '-79%', '-89%', '-90%', '-95%', '+78%']
})

print("\n📊 MOCK PERFORMANCE SUMMARY")
print("="*60)
print(summary.to_string(index=False))
summary.to_csv('mock_performance_summary.csv', index=False)
print("\n✅ Created mock_performance_summary.csv")

print("\n" + "="*60)
print("🎯 PRACTICE COMPLETE! You now have mock data to:")
print("   1. Practice running collect_metrics.py")
print("   2. See how your graphs will look")
print("   3. Fill in your presentation templates")
print("   4. Practice your 4-minute segment")
print("="*60)