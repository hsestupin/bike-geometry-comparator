import {
  AsyncDuckDB,
  AsyncDuckDBConnection,
  createWorker,
  DuckDBBundles,
  getJsDelivrBundles
} from "@duckdb/duckdb-wasm";

const JSDELIVR_BUNDLES = getJsDelivrBundles()

export async function connectDuckDb(): Promise<AsyncDuckDBConnection> {
  const duckDb = await instantiateDuckDB(JSDELIVR_BUNDLES)
  const connection = duckDb.connect()
  return connection
}

export async function instantiateDuckDB(duckDbBundles: DuckDBBundles): Promise<AsyncDuckDB> {
  const [duckdb] = await Promise.all([import('@duckdb/duckdb-wasm')])

  const bundle = await duckdb.selectBundle(duckDbBundles)
  const worker = await createWorker(bundle.mainWorker!)
  const logger = process.env.NODE_ENV === 'development' ? new duckdb.ConsoleLogger() : new duckdb.VoidLogger()
  const db = new duckdb.AsyncDuckDB(logger, worker)
  await db.instantiate(bundle.mainModule, bundle.pthreadWorker)

  return db
}