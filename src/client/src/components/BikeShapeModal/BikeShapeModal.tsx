import { useCallback, useEffect } from 'react';
import { createPortal } from 'react-dom';
import BikeShape from '@/components/BikeRenderer/BikeShape';
import { Geometry } from '@/components/BikeRenderer/bikeGeometry';
import styles from './BikeShapeModal.module.css';

type BikeShapeModalProps = {
  title: string;
  geometry: Geometry;
  referenceGeometry?: Geometry;
  onClose: () => void;
};

export default function BikeShapeModal({title, geometry, referenceGeometry, onClose}: BikeShapeModalProps) {
  const handleKey = useCallback((e: KeyboardEvent) => {
    if (e.key === 'Escape') onClose();
  }, [onClose]);

  useEffect(() => {
    document.addEventListener('keydown', handleKey);
    return () => document.removeEventListener('keydown', handleKey);
  }, [handleKey]);

  return createPortal(
    <div className={styles.backdrop} onClick={onClose}>
      <div className={styles.panel} onClick={e => e.stopPropagation()}>
        <div className={styles.header}>
          <h3 className={styles.title}>{title}</h3>
          <button className={styles.close} onClick={onClose} aria-label="Close">✕</button>
        </div>
        <div className={styles.body}>
          <BikeShape geometry={geometry} referenceGeometry={referenceGeometry} showDimensions={true}/>
        </div>
      </div>
    </div>,
    document.body
  );
}
