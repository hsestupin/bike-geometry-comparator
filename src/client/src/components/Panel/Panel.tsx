import { PropsWithChildren } from 'react';
import styles from './Panel.module.css';

type PanelProps = PropsWithChildren<{ className?: string } & React.HTMLAttributes<HTMLDivElement>>;

export default function Panel({ children, className = '', ...rest }: PanelProps) {
  return (
    <div className={`${styles.panel} ${className}`} {...rest}>
      {children}
    </div>
  );
}
