import MainPage from './MainPage';
import {createDataService, DataService} from "@/data/dataService";
import {useEffect, useState} from "react";

const FILE_PATH = "/database.csv"

export default function App() {
  const [dataService, setDataService] = useState<DataService | null>(null);

  useEffect(() => {
    const baseUrl = import.meta.env.BASE_URL.replace(/\/$/, '');
    const url = `${location.origin}${baseUrl}${FILE_PATH}`;
    createDataService(url).then(setDataService);
  }, [])

  return (
    dataService && <MainPage dataService={dataService}/>
  );
}
