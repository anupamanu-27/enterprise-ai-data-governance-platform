from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def main() -> None:
    project_root = Path("/workspace")
    source_file = project_root / "data" / "samples" / "marketing_campaigns.csv"
    output_dir = project_root / "data" / "curated" / "delta" / "campaign_summary"

    spark = (
        SparkSession.builder.appName("build-campaign-delta-table")
        .master("local[*]")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
        .getOrCreate()
    )

    try:
        campaigns = (
            spark.read.option("header", "true")
            .option("inferSchema", "true")
            .csv(str(source_file))
        )

        campaign_summary = (
            campaigns.withColumn("budget", F.col("budget").cast("double"))
            .groupBy("region", "channel")
            .agg(
                F.count("campaign_id").alias("campaign_count"),
                F.round(F.sum("budget"), 2).alias("total_budget"),
                F.round(F.avg("budget"), 2).alias("average_budget"),
            )
            .withColumn("lakehouse_layer", F.lit("curated"))
            .orderBy("region", "channel")
        )

        campaign_summary.write.format("delta").mode("overwrite").save(str(output_dir))

        reloaded = spark.read.format("delta").load(str(output_dir))
        print(f"Delta campaign summary written to {output_dir}")
        print(f"Delta row count: {reloaded.count()}")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()

