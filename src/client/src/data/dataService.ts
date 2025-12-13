import { Bike } from "@/types/Bike";
import { AsyncDuckDBConnection, DuckDBDataProtocol } from "@duckdb/duckdb-wasm";
import { connectDuckDb } from "@/data/duckDb";
import { DataType, Field, Table } from "apache-arrow";
import { Statistics } from "@/types/Statistics";
import { Bound } from "@/types/Bound";

export interface DataService {
  allBikes(): Promise<Bike[]>
  findBikes(brands?: string[], reachBound?: Bound, stackBound?: Bound): Promise<Bike[]>
  brands(): Promise<string[]>
  statistics(): Promise<Statistics>
}

export async function createDataService(filePath: string, tableName: string = "bikes_table"): Promise<DataService> {
  const connection = await connectDuckDb();
  await connection.bindings.registerFileURL(tableName, filePath, DuckDBDataProtocol.HTTP, false)
  await connection.insertCSVFromPath(tableName, {name: tableName});
  return new DuckDbDataService(tableName, connection);
}

export class DuckDbDataService implements DataService {
  private tableName: string
  private connection: AsyncDuckDBConnection;

  constructor(tableName: string, connection: AsyncDuckDBConnection) {
    this.tableName = tableName;
    this.connection = connection;
  }

  async allBikes(): Promise<Bike[]> {
    const sql = `SELECT * FROM ${this.tableName}`;
    return this.runBikesQuery(sql);
  }

  async findBikes(brands?: string[], reachBound?: Bound, stackBound?: Bound): Promise<Bike[]> {
    const whereClauses: string[] = [];
    if (brands) {
      whereClauses.push(`brand IN (${brands.map(brand => `'${brand}'`).join(', ')})`);
    }
    if (reachBound) {
      whereClauses.push(`reach BETWEEN ${reachBound.min} AND ${reachBound.max}`);
    }
    if (stackBound) {
      whereClauses.push(`stack BETWEEN ${stackBound.min} AND ${stackBound.max}`);
    }

    if (whereClauses.length === 0) {
      return this.allBikes();
    }

    const whereClause = whereClauses.join(' AND ');
    const sql = `SELECT * FROM ${this.tableName} WHERE ${whereClause}`;
    return this.runBikesQuery(sql);
  }

  async brands(): Promise<string[]> {
    const sql = `SELECT DISTINCT brand FROM ${this.tableName}`;
    const result = await this.connection.query(sql);
    const data = this.parseResult(result);
    return data.map(row => row['brand'] as string);
  }

  async statistics(): Promise<Statistics> {
    const sql = `SELECT MIN(stack) AS min_stack, MAX(stack) AS max_stack, MIN(reach) AS min_reach, MAX(reach) AS max_reach FROM ${this.tableName}`;
    const result = await this.connection.query(sql);
    const data = this.parseResult(result);
    return {
      stack: { min: data[0]['min_stack'] as number, max: data[0]['max_stack'] as number },
      reach: { min: data[0]['min_reach'] as number, max: data[0]['max_reach'] as number },
    }
  }

  private async runBikesQuery(sql: string): Promise<Bike[]> {
    const result = await this.connection.query(sql);
    const data = this.parseResult(result);
    const bikes: Bike[] = [];

    for (const row of data) {
      bikes.push({
        brand: row['brand'] as string,
        model: row['model'] as string,
        reach: row['reach'] as number,
        size: row['size'] as string,
        stack: row['stack'] as number,
        year: row['year'] as number,
      });
    }

    return Promise.resolve(bikes);
  }

  private parseResult(table: Table<any>): Record<string, string | number | null>[] {
    const columns = table.schema.fields;
    const data: Record<string, string | number | null>[] = [];

    for (const arrowRow of table) {
      const row = arrowRow.toArray();
      const rowData: Record<string, string | number | null> = {}
      for (let i = 0; i < columns.length; i++) {
        const column = columns[i];
        const value = this.parseValue(row[i], column);
        rowData[column.name] = value;
      }
      data.push(rowData);
    }

    return data;
  }

  private parseValue(value: any, column: Field<any>): string | number | null {
    if (value === null) {
      return null;
    }

    if (DataType.isInt(column.type) || DataType.isFloat(column.type)) {
      return Number(value);
    }

    return String(value);
  }
}
