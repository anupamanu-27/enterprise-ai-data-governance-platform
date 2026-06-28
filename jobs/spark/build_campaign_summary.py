from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def main() -> None:
    project_root = Path("/workspace")
    source_file = project_root / "data" / "samples" / "marketing_campaigns.csv"
    output_dir = project_root / "data" / "curated" / "campaign_summary"

    spark = (
        SparkSession.builder.appName("build-campaign-summary")
        .master("local[*]")
        .getOrCreate()
    )

    try:
        campaigns = (
            spark.read.option("header", "true")
            .option("inferSchema", "true")
            .csv(str(source_file))
        )

        curated_summary = (
            campaigns.withColumn("budget", F.col("budget").cast("double"))
            .groupBy("region", "channel")
            .agg(
                F.count("campaign_id").alias("campaign_count"),
                F.round(F.sum("budget"), 2).alias("total_budget"),
                F.round(F.avg("budget"), 2).alias("average_budget"),
            )
            .orderBy("region", "channel")
        )

        curated_summary.coalesce(1).write.mode("overwrite").option(
            "header",
            "true",
        ).csv(str(output_dir))

        print(f"Curated campaign summary written to {output_dir}")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()

