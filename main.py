from ec2 import get_instances
from s3 import list_buckets
from lambda_fn import list_functions
from cloudwatch import get_cpu
from cost import get_total_cost, get_service_usage_and_cost
from sns_alert import send_alert
from config import COST_THRESHOLD, CPU_THRESHOLD

def check_idle(instances):
    print("\nChecking Idle Instances...")

    for inst in instances:
        data = get_cpu(inst)

        if not data:
            msg = f"⚠️ EC2 {inst} has no CPU data (treating as idle)"
            print(msg)
            send_alert(msg)
            continue

        cpu = data[0]['Average']

        if cpu < CPU_THRESHOLD:
            msg = f"⚠️ EC2 {inst} is idle (CPU {cpu}%)"
            print(msg)
            send_alert(msg)

def check_cost():
    cost = get_total_cost()
    print(f"\nCurrent Cost: ${cost}")

    if cost > COST_THRESHOLD:
        msg = f"⚠️ Cost exceeded! Current: ${cost}"
        send_alert(msg)
    else:
        print("Cost under control")

def main():
    while True:
        print("\n===== AWS MONITOR CLI =====")
        print("1. EC2 Monitor")
        print("2. S3 Monitor")
        print("3. Lambda Monitor")
        print("4. Cost Check")
        print("5. Service usage/cost report")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            instances = get_instances()
            check_idle(instances)

        elif choice == "2":
            list_buckets()

        elif choice == "3":
            list_functions()

        elif choice == "4":
            check_cost()

        elif choice == "5":
            service = input("Enter service name (EC2/S3/Lambda or leave blank for all): ").strip()
            report = get_service_usage_and_cost(service_name=service if service else None)
            print("\nname | location | usage | bill")
            for item in report:
                print(f"{item['name']} | {item['location']} | {item['usage']} | ${item['bill']:.2f}")

        elif choice == "6":
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()