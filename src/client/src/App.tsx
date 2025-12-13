import MainPage from './MainPage';
import { createDataService, DataService } from "@/data/dataService";
import { useEffect, useState } from "react";

const FILE_PATH = "/database.csv"

export default function App() {
  const [dataService, setDataService] = useState<DataService | null>(null);

  useEffect(() => {
    createDataService(`${location.origin}${FILE_PATH}`).then(setDataService);
  }, [])

  return (
    dataService && <MainPage dataService={dataService}/>
  );
}
