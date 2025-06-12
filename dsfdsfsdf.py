cat << 'EOF' > peacock_mixed_content_tester.py
import os
import json
import time
import requests
import re
from datetime import datetime

class PeacockMixedContentTester:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.contenders = ["llama-3.1-8b-instant", "gemma2-9b-it", "llama3-8b-8192"]
        self.results = {}
    
    def send_request(self, model, prompt, test_name):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 1500
        }
        
        try:
            start_time = time.time()
            response = requests.post(self.base_url, headers=headers, json=payload)
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                return {
                    "success": True,
                    "response": content,
                    "response_time": end_time - start_time,
                    "test_name": test_name,
                    "model": model
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "test_name": test_name,
                    "model": model
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "test_name": test_name,
                "model": model
            }
    
    def parse_mixed_content(self, response_text):
        scores = {
            "explanation_quality": 0,
            "code_extraction": 0,
            "json_extraction": 0,
            "structure_recognition": 0,
            "total_score": 0
        }
        
        # 1. Explanation Quality
        explanation_indicators = [
            "this code", "the function", "here's how", "this works by",
            "the purpose", "you can", "this will", "it does", "explanation"
        ]
        explanation_found = sum(1 for indicator in explanation_indicators if indicator in response_text.lower())
        scores["explanation_quality"] = min(explanation_found * 10, 50)
        
        # 2. Code Block Extraction
        code_blocks = re.findall(r'```[\w]*\n(.*?)\n```', response_text, re.DOTALL)
        if code_blocks:
            scores["code_extraction"] = 30
            if len(code_blocks) > 1:
                scores["code_extraction"] += 10
            code_text = ' '.join(code_blocks)
            if any(keyword in code_text for keyword in ['def ', 'function', 'const ', 'let ', 'var ']):
                scores["code_extraction"] += 10
        
        # 3. JSON Extraction
        try:
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            json_matches = re.findall(json_pattern, response_text, re.DOTALL)
            for match in json_matches:
                try:
                    json.loads(match)
                    scores["json_extraction"] = 25
                    break
                except:
                    scores["json_extraction"] = 10
                    continue
        except:
            pass
        
        # 4. Structure Recognition
        structure_points = 0
        if re.search(r'^#+\s+', response_text, re.MULTILINE):
            structure_points += 5
        if re.search(r'\*\*.*?\*\*', response_text):
            structure_points += 5
        if re.search(r'^\s*[-•*]\s+', response_text, re.MULTILINE):
            structure_points += 5
        if re.search(r'^\s*\d+\.\s+', response_text, re.MULTILINE):
            structure_points += 5
        if '```' in response_text and any(word in response_text.lower() for word in ['explanation', 'analysis', 'summary']):
            structure_points += 10
        
        scores["structure_recognition"] = structure_points
        scores["total_score"] = sum([
            scores["explanation_quality"],
            scores["code_extraction"], 
            scores["json_extraction"],
            scores["structure_recognition"]
        ])
        
        return scores
    
    def get_mixed_content_prompts(self):
        prompts = {
            "code_analysis_mixed": '''
Analyze this Python function and provide:

1. A natural language explanation of what the code does
2. The corrected/improved code in a code block
3. A JSON summary of the analysis

```python
def calculate_discount(price, customer_type):
    if customer_type == "premium":
        return price * 0.8
    elif customer_type == "regular":
        return price * 0.9
    else:
        return price
        I need to understand this code, see an improved version, and get structured data about the analysis.
        "feature_implementation":
        I want to add a "favorites" feature to my web app. Please provide:

An explanation of how favorites typically work
Sample code for the backend API (Python/Flask)
Sample code for the frontend (JavaScript)
A JSON configuration object for the feature

Make sure I can understand the concept, see the implementation, and have structured data for configuration.
 "bug_fix_analysis":
 This code has a bug where users can't log in. Please help by providing:

An explanation of what might be wrong
The fixed code in code blocks
JSON data showing the before/after comparison
function loginUser(username, password) {
    if (username && password) {
        fetch('/api/login', {
            method: 'POST',
            body: JSON.stringify({user: username, pass: password})
        }).then(response => {
            if (response.status === 200) {
                window.location = '/dashboard';
            }
        });
    }
}
I need to understand the problem, see the solution, and have structured data about the changes.
 "architecture_explanation": 
 Explain microservices architecture and provide:

A clear explanation of what microservices are and their benefits
Sample code showing a simple microservice (Python)
Sample Docker configuration
JSON configuration for service discovery

I need to learn the concept, see practical examples, and have configuration data.
"api_design_mixed":
Help me design a REST API for a blog system. Please provide:

An explanation of RESTful API design principles
Sample API endpoint code (Node.js/Express)
Example request/response data
JSON API documentation structure

I want to understand the principles, see working code, and have structured documentation.
'''
}
return prompts

def run_mixed_content_tests(self):
    prompts = self.get_mixed_content_prompts()
    
    print("="*80)
    print("PEACOCK MIXED CONTENT INTELLIGENCE TEST")
    print("="*80)
    print("Testing ability to generate and parse:")
    print("  - Natural language explanations")
    print("  - Code blocks")
    print("  - Structured JSON data")
    print("  - Organized content structure")
    print("="*80)
    
    all_results = {}
    
    for test_name, prompt in prompts.items():
        print(f"\nTESTING: {test_name.upper()}")
        print("="*60)
        
        test_results = {}
        
        for model in self.contenders:
            print(f"\nTesting {model}...")
            result = self.send_request(model, prompt, test_name)
            
            if result["success"]:
                content_scores = self.parse_mixed_content(result["response"])
                result.update(content_scores)
                
                print(f"  Response Time: {result['response_time']:.2f}s")
                print(f"  Explanation: {content_scores['explanation_quality']}/50")
                print(f"  Code: {content_scores['code_extraction']}/50") 
                print(f"  JSON: {content_scores['json_extraction']}/25")
                print(f"  Structure: {content_scores['structure_recognition']}/25")
                print(f"  TOTAL: {content_scores['total_score']}/150")
            else:
                result.update({
                    "explanation_quality": 0,
                    "code_extraction": 0,
                    "json_extraction": 0,
                    "structure_recognition": 0,
                    "total_score": 0
                })
                print(f"  FAILED: {result['error']}")
            
            test_results[model] = result
            time.sleep(1)
        
        winner = max(test_results.items(), key=lambda x: x[1].get('total_score', 0))
        print(f"\nTEST WINNER: {winner[0]} ({winner[1].get('total_score', 0)}/150)")
        
        all_results[test_name] = test_results
    
    self.results = all_results
    return all_results

def analyze_overall_results(self):
    print("\n" + "="*80)
    print("MIXED CONTENT CHAMPIONSHIP ANALYSIS")
    print("="*80)
    
    model_totals = {model: {
        "total_score": 0,
        "wins": 0,
        "avg_explanation": 0,
        "avg_code": 0,
        "avg_json": 0,
        "avg_structure": 0,
        "test_count": 0
    } for model in self.contenders}
    
    for test_name, test_results in self.results.items():
        print(f"\n{test_name.upper()}:")
        
        test_winner = max(test_results.items(), key=lambda x: x[1].get('total_score', 0))
        model_totals[test_winner[0]]["wins"] += 1
        
        for model, result in test_results.items():
            if result.get("success", False):
                model_totals[model]["total_score"] += result.get("total_score", 0)
                model_totals[model]["avg_explanation"] += result.get("explanation_quality", 0)
                model_totals[model]["avg_code"] += result.get("code_extraction", 0)
                model_totals[model]["avg_json"] += result.get("json_extraction", 0)
                model_totals[model]["avg_structure"] += result.get("structure_recognition", 0)
                model_totals[model]["test_count"] += 1
            
            score = result.get("total_score", 0)
            status = "WINNER" if model == test_winner[0] else "      "
            print(f"  {status} {model:25} | Score: {score:3d}/150")
    
    print("\n" + "="*80)
    print("FINAL MIXED CONTENT RANKINGS")
    print("="*80)
    
    final_rankings = []
    for model, totals in model_totals.items():
        if totals["test_count"] > 0:
            avg_total = totals["total_score"] / totals["test_count"]
            avg_explanation = totals["avg_explanation"] / totals["test_count"]
            avg_code = totals["avg_code"] / totals["test_count"]
            avg_json = totals["avg_json"] / totals["test_count"]
            avg_structure = totals["avg_structure"] / totals["test_count"]
            
            final_rankings.append((model, totals["wins"], avg_total, {
                "explanation": avg_explanation,
                "code": avg_code,
                "json": avg_json,
                "structure": avg_structure
            }))
    
    final_rankings.sort(key=lambda x: (x[1], x[2]), reverse=True)
    
    for rank, (model, wins, avg_score, breakdown) in enumerate(final_rankings, 1):
        print(f"\n{rank}. {model}")
        print(f"   Test Wins: {wins}/{len(self.results)}")
        print(f"   Average Score: {avg_score:.1f}/150")
        print(f"   Explanation: {breakdown['explanation']:.1f}/50")
        print(f"   Code: {breakdown['code']:.1f}/50")
        print(f"   JSON: {breakdown['json']:.1f}/25")
        print(f"   Structure: {breakdown['structure']:.1f}/25")
    
    champion = final_rankings[0]
    print(f"\nMIXED CONTENT CHAMPION: {champion[0]}")
    print(f"Best at handling explanations + code + structured data")
    
    print(f"\nPEACOCK IMPLEMENTATION RECOMMENDATIONS:")
    print(f"   Primary Model: {champion[0]}")
    print(f"   Strengths: Mixed content generation and parsing")
    print(f"   Use for: Complex Peacock workflows requiring multiple content types")
    
    return champion[0], final_rankings
    if name == "main":
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
print("Set GROQ_API_KEY environment variable")
exit(1)
tester = PeacockMixedContentTester(api_key)

results = tester.run_mixed_content_tests()
champion, rankings = tester.analyze_overall_results()

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"peacock_mixed_content_results_{timestamp}.json"

with open(filename, 'w') as f:
    json.dump({
        "champion": champion,
        "rankings": rankings,
        "detailed_results": tester.results,
        "timestamp": timestamp
    }, f, indent=2)

print(f"\nResults saved to: {filename}")
print(f"{champion} is the Mixed Content Champion!")
EOF