from app.run_store import RunStore


def main():

    store = RunStore()

    runs = store.list_runs()

    print("=" * 80)
    print("AVAILABLE EVALUATION RUNS")
    print("=" * 80)

    for run in runs:
        print(run)


if __name__ == "__main__":
    main()