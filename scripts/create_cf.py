import json
import time
import subprocess
import sys

def create_cf_dist():
    profile = "mediusa"
    bucket_name = "avhandymanpros-v3"
    # Note: Assuming us-east-1 for simplicity, adjust if needed
    origin_domain = f"{bucket_name}.s3-website-us-east-1.amazonaws.com"
    caller_ref = f"{bucket_name}-{int(time.time())}"
    
    config = {
        "CallerReference": caller_ref,
        "Origins": {
            "Quantity": 1,
            "Items": [
                {
                    "Id": f"S3-{bucket_name}",
                    "DomainName": origin_domain,
                    "CustomOriginConfig": {
                        "HTTPPort": 80,
                        "HTTPSPort": 443,
                        "OriginProtocolPolicy": "http-only"
                    }
                }
            ]
        },
        "DefaultCacheBehavior": {
            "TargetOriginId": f"S3-{bucket_name}",
            "ForwardedValues": {
                "QueryString": False,
                "Cookies": {
                    "Forward": "none"
                }
            },
            "TrustedSigners": {
                "Enabled": False,
                "Quantity": 0
            },
            "ViewerProtocolPolicy": "redirect-to-https",
            "MinTTL": 0,
            "DefaultTTL": 86400,
            "MaxTTL": 31536000
        },
        "Comment": "AV Handyman Pros Production",
        "Enabled": True,
        "DefaultRootObject": "index.html"
    }
    
    config_path = "/Users/mediusa/NOVA/Repos/Handy Man Services/scripts/cf_config.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    cmd = [
        "aws", "cloudfront", "create-distribution",
        "--distribution-config", f"file://{config_path}",
        "--profile", profile
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        dist_id = data["Distribution"]["Id"]
        domain_name = data["Distribution"]["DomainName"]
        print(f"DIST_ID={dist_id}")
        print(f"DOMAIN={domain_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    create_cf_dist()
