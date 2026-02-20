import { useCallback, useEffect, useState } from 'react';
import Range from './components/Range/Range';
import BrandFilter from './components/Filters/BrandFilter';
import BikesTable from './components/BikesTable/BikesTable';
import BikeDetailsPanel from './components/BikeDetailsPanel/BikeDetailsPanel';
import { Bike } from './types/Bike';
import styles from './App.module.css';
import { DataService } from "@/data/dataService";
import { EMPTY_STATISTICS, Statistics } from "@/types/Statistics";
import { Bound, equalBounds } from "@/types/Bound";
import { BikeDetailedInfo } from "@/types/BikeDetailedInfo";

type Props = { dataService: DataService };

export default function MainPage(props: Props) {
  const {dataService} = props;
  const [allBikes, setAllBikes] = useState<Bike[]>([]);
  const [allBrands, setAllBrands] = useState<string[]>([]);
  const [filteredBikes, setFilteredBikes] = useState<Bike[]>([]);
  const [statistics, setStatistics] = useState<Statistics>(EMPTY_STATISTICS)
  const [stack, setStack] = useState<Bound>(statistics.stack);
  const [reach, setReach] = useState<Bound>(statistics.reach);
  const [selectedBrands, setSelectedBrands] = useState<Set<string>>(new Set());
  const [selectedBike, setSelectedBike] = useState<BikeDetailedInfo | null>(null);
  const [pinnedBike, setPinnedBike] = useState<BikeDetailedInfo | null>(null);

  const toggleBrand = (brand: string) => {
    setSelectedBrands(prev => {
      const next = new Set(prev);
      if (next.has(brand)) next.delete(brand); else next.add(brand);
      return next;
    });
  };

  const clearAll = () => {
    setStack(statistics.stack);
    setReach(statistics.reach);
    setSelectedBrands(new Set());
  };

  useEffect(() => {
    const brandFilter = selectedBrands.size > 0 ? [...selectedBrands] : undefined;
    const stackFilter = !equalBounds(statistics.stack, stack) ? stack : undefined;
    const reachFilter = !equalBounds(statistics.reach, reach) ? reach : undefined;
    if (brandFilter || stackFilter || reachFilter) {
      dataService.findBikes(brandFilter, reachFilter, stackFilter).then(setFilteredBikes);
    } else {
      setFilteredBikes(allBikes);
    }
  }, [allBikes, stack, reach, selectedBrands]);

  useEffect(() => {
    dataService.brands().then(setAllBrands);
    dataService.allBikes().then(bikes => {
      setAllBikes(bikes);
      setFilteredBikes(bikes);
    });
    dataService.statistics().then(statistics => {
      setStatistics(statistics);
      setStack(statistics.stack);
      setReach(statistics.reach);
    });
  }, [dataService]);

  const handleSelectedBike = useCallback((bike: Bike) => {
    dataService.detailedInfo(bike.brand, bike.model, bike.year, bike.size).then(setSelectedBike);
  }, [])

  const handlePinBike = useCallback((bike: BikeDetailedInfo) => {
    setPinnedBike(prev => prev !== null ? null : bike);
  }, []);

  const appClass = `${styles.app} ${selectedBike ? styles.appWithDetails : ''}`;

  return (
    <div className={appClass}>
      <div className={styles.left}>
        <aside className={styles.sidebar} aria-label="Filters sidebar">
          <div className={styles.filtersInner}>
            <Range min={statistics.stack.min} max={statistics.stack.max} value={stack} onChange={setStack} label="Stack"
                   unit=" mm"/>
            <Range min={statistics.reach.min} max={statistics.reach.max} value={reach} onChange={setReach} label="Reach"
                   unit=" mm"/>
            <BrandFilter brands={allBrands} selected={selectedBrands} onToggle={toggleBrand}/>
          </div>
          <div className={styles.sidebarFooter}>
            <button className={styles.clearAll} onClick={clearAll}>Clear filters</button>
          </div>
        </aside>
      </div>
      <div className={styles.center}>
        <div className={styles.centerContent}>
          <BikesTable bikes={filteredBikes} onSelect={handleSelectedBike}/>
        </div>
      </div>
      {selectedBike && (
        <div className={styles.right}>
          <BikeDetailsPanel bike={selectedBike} pinnedBike={pinnedBike} onPin={handlePinBike} onClose={() => setSelectedBike(null)}/>
        </div>
      )}
    </div>
  );
}
