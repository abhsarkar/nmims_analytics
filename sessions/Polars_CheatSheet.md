# Polars Quick Reference — QuickKart Labs

A trimmed-down reference covering only what you need for this class. For everything else, see the
[full Polars docs](https://docs.pola.rs).

---

## Setup (do this once per notebook)

```python
import sys, subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "polars"])
import polars as pl
```

`sys.executable` installs into the exact Python your notebook's kernel is using — avoids the
"pip said it worked but import still fails" trap.

---

## Reading data: eager vs. lazy

| Call | Returns | When it runs |
|---|---|---|
| `pl.read_csv(path)` | `DataFrame` | **immediately** — loads the whole file into memory |
| `pl.scan_csv(path)` | `LazyFrame` | **not yet** — just builds a plan |

Rule of thumb: default to `scan_csv` + `.collect()` at the end. Polars optimizes the whole
pipeline before running it.

```python
lazy = pl.scan_csv("orders.csv")   # nothing runs yet
result = lazy.collect()            # NOW it runs
```

---

## The core pipeline: filter → group → aggregate → sort

```python
result = (
    pl.scan_csv("orders.csv")
      .filter(pl.col("OrderValue") > 500)              # keep rows matching a condition
      .group_by("Region")                                # bucket rows by a column
      .agg(pl.col("OrderValue").sum().alias("Total"))     # aggregate within each bucket
      .sort("Total", descending=True)                    # order the result
      .collect()                                          # trigger the run
)
```

- `pl.col("X")` — refers to column X. Almost everything in Polars starts with this.
- `.alias("Name")` — renames the result of an expression.
- Common aggregations: `.sum()`, `.mean()`, `.median()`, `.count()`, `.min()`, `.max()`

---

## Adding / transforming columns

```python
df.with_columns(
    pl.col("OrderDate").str.to_date().alias("Date"),   # parse a string into a real date
    pl.col("OrderDate").str.slice(0, 7).alias("Month")  # "YYYY-MM-DD" -> "YYYY-MM"
)
```

Conditional column (like a spreadsheet IF):

```python
df.with_columns(
    pl.when(pl.col("OrderValue") > 500)
      .then(pl.lit("Big"))
      .otherwise(pl.lit("Small"))
      .alias("OrderSize")
)
```

---

## Joining two tables

```python
combined = df1.join(df2, on="Region")   # inner join by default
```

---

## Getting values out

```python
df["Region"].to_list()      # column -> Python list
df["Total"].to_numpy()      # column -> numpy array
df.row(0, named=True)       # first row as a dict-like object, e.g. row["Region"]
```

---

## Peeking at what Polars will actually do

```python
lazy_query.explain()   # prints the optimized query plan — useful for seeing filter/predicate pushdown
```

---

## Cheat sheet: the 90% you'll use in this class

| Task | Polars |
|---|---|
| Load a file (fast, optimized) | `pl.scan_csv(path)` |
| Load a file (immediate) | `pl.read_csv(path)` |
| Keep matching rows | `.filter(pl.col("X") > 5)` |
| Add/replace a column | `.with_columns(pl.col("X")....alias("Y"))` |
| Group + summarize | `.group_by("X").agg(pl.col("Y").sum())` |
| Sort | `.sort("X", descending=True)` |
| Run a lazy pipeline | `.collect()` |
| Combine two tables | `.join(other, on="X")` |
| If/else logic | `pl.when(cond).then(a).otherwise(b)` |

**Golden rule:** if you wrote `pl.scan_csv(...)`, nothing happens until you call `.collect()`.