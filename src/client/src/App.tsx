import { useMemo, useState } from 'react';
import Panel from './components/Panel/Panel';
import Range from './components/Range/Range';
import BrandFilter from './components/Filters/BrandFilter';
import BikesTable from './components/BikesTable/BikesTable';
import BikeDetailsPanel from './components/BikeDetailsPanel/BikeDetailsPanel';
import { bikes as allBikes, brands as allBrands, stackBounds, reachBounds } from './data/bikes';
import { Bike } from './types/Bike';
import styles from './App.module.css';

export default function App() {
  const [stack, setStack] = useState<[number, number]>([stackBounds.min, stackBounds.max]);
  const [reach, setReach] = useState<[number, number]>([reachBounds.min, reachBounds.max]);
  const [selectedBrands, setSelectedBrands] = useState<Set<string>>(new Set());
  const [selectedBike, setSelectedBike] = useState<Bike | null>(null);

  const filtered = useMemo(() => {
    return allBikes.filter(b =>
      b.stack >= stack[0] && b.stack <= stack[1] &&
      b.reach >= reach[0] && b.reach <= reach[1] &&
      (selectedBrands.size === 0 || selectedBrands.has(b.brand))
    );
  }, [stack, reach, selectedBrands]);

  const toggleBrand = (brand: string) => {
    setSelectedBrands(prev => {
      const next = new Set(prev);
      if (next.has(brand)) next.delete(brand); else next.add(brand);
      return next;
    });
  };

  const clearBrands = () => setSelectedBrands(new Set());
  const clearAll = () => {
    setStack([stackBounds.min, stackBounds.max]);
    setReach([reachBounds.min, reachBounds.max]);
    setSelectedBrands(new Set());
  };

  const appClass = `${styles.app} ${selectedBike ? styles.appWithDetails : ''}`;
  return (
    <div className={appClass}>
      <div className={styles.left}>
        <aside className={styles.sidebar} aria-label="Filters sidebar">
          <div className={styles.filtersInner}>
            <Range min={stackBounds.min} max={stackBounds.max} value={stack} onChange={setStack} label="Stack" unit=" mm" />
            <Range min={reachBounds.min} max={reachBounds.max} value={reach} onChange={setReach} label="Reach" unit=" mm" />
            <BrandFilter brands={allBrands} selected={selectedBrands} onToggle={toggleBrand} />
          </div>
          <div className={styles.sidebarFooter}>
            <button className={styles.clearAll} onClick={clearAll}>Clear</button>
          </div>
        </aside>
      </div>
      <div className={styles.center}>
        <div className={styles.centerContent}>
          <BikesTable bikes={filtered} onSelect={setSelectedBike} />
        </div>
      </div>
      {selectedBike && (
        <div className={styles.right}>
          <BikeDetailsPanel bike={selectedBike} onClose={() => setSelectedBike(null)} />
        </div>
      )}
    </div>
  );
}
