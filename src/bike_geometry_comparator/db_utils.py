import duckdb


def fetchall_strings(sql, conn=None) -> list[str]:
    if conn:
        with conn.cursor() as cur:
            return [res for (res,) in cur.execute(sql).fetchall()]
    else:
        return [res for (res,) in duckdb.execute(sql).fetchall()]
