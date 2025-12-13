import { useMemo, useState } from 'react';
import { Bike } from '@/types/Bike';
import styles from './BikesTable.module.css';

type Props = {
  bikes: Bike[];
  onSelect: (bike: Bike) => void;
};

type SortKey = keyof Pick<Bike, 'brand' | 'model' | 'year' | 'size' | 'stack' | 'reach'>;
type SortDir = 'asc' | 'desc' | null;

export default function BikesTable({ bikes, onSelect }: Props) {
  const [sortKey, setSortKey] = useState<SortKey | null>(null);
  const [sortDir, setSortDir] = useState<SortDir>(null);

  const cycleDir = (key: SortKey) => {
    if (sortKey !== key) {
      setSortKey(key);
      setSortDir('asc');
      return;
    }
    // same column: asc -> desc -> null
    setSortDir(prev => (prev === 'asc' ? 'desc' : prev === 'desc' ? null : 'asc'));
    // if next is null, also clear sortKey to reflect reset
    setSortKey(prev => (sortDir === 'desc' ? null : prev));
  };

  const sorted = useMemo(() => {
    if (!sortKey || !sortDir) return bikes;
    const arr = [...bikes];
    arr.sort((a, b) => {
      const va = a[sortKey];
      const vb = b[sortKey];
      let res = 0;
      if (typeof va === 'number' && typeof vb === 'number') {
        res = va - vb;
      } else {
        res = String(va).localeCompare(String(vb));
      }
      return sortDir === 'asc' ? res : -res;
    });
    return arr;
  }, [bikes, sortKey, sortDir]);

  const sortIndicator = (key: SortKey) => {
    if (sortKey !== key || !sortDir) return '';
    return sortDir === 'asc' ? ' ▲' : ' ▼';
  };

  const ariaSortFor = (key: SortKey): 'none' | 'ascending' | 'descending' => {
    if (sortKey !== key || !sortDir) return 'none';
    return sortDir === 'asc' ? 'ascending' : 'descending';
  };

  return (
    <div className={styles.wrap}>
      <table className={styles.table}>
        <thead>
          <tr>
            <th aria-sort={ariaSortFor('brand')}>
              <button
                className={styles.sortBtn}
                onClick={() => cycleDir('brand')}
              >Brand{sortIndicator('brand')}</button>
            </th>
            <th aria-sort={ariaSortFor('model')}>
              <button
                className={styles.sortBtn}
                onClick={() => cycleDir('model')}
              >Model{sortIndicator('model')}</button>
            </th>
            <th aria-sort={ariaSortFor('year')}>
              <button
                className={styles.sortBtn}
                onClick={() => cycleDir('year')}
              >Year{sortIndicator('year')}</button>
            </th>
            <th aria-sort={ariaSortFor('size')}>
              <button
                className={styles.sortBtn}
                onClick={() => cycleDir('size')}
              >Size{sortIndicator('size')}</button>
            </th>
            <th aria-sort={ariaSortFor('stack')}>
              <button
                className={styles.sortBtn}
                onClick={() => cycleDir('stack')}
              >Stack{sortIndicator('stack')}</button>
            </th>
            <th aria-sort={ariaSortFor('reach')}>
              <button
                className={styles.sortBtn}
                onClick={() => cycleDir('reach')}
              >Reach{sortIndicator('reach')}</button>
            </th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((b) => (
            <tr key={`${b.brand}-${b.model}-${b.size}-${b.year}`}>
              <td>{b.brand}</td>
              <td>
                <button className={styles.modelBtn} onClick={() => onSelect(b)}>{b.model}</button>
              </td>
              <td>{b.year}</td>
              <td>{b.size}</td>
              <td>{b.stack}</td>
              <td>{b.reach}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {bikes.length === 0 && <div className={styles.empty}>No bikes match these filters.</div>}
    </div>
  );
}
