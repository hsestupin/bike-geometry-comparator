import { DEFAULT_GEOMETRY, Geometry } from "@/components/BikeRenderer/bikeGeometry";
import { renderBikeShapeSvg } from "@/components/BikeRenderer/bikeSvgRenderer";

import styles from './BikeShape.module.css';

type Props = {
  geometry?: Geometry
};

export default function BikeShape(props: Props) {
  const {geometry = DEFAULT_GEOMETRY} = props;
  return (<div
    className={styles.root}
    dangerouslySetInnerHTML={{
      __html: renderBikeShapeSvg(geometry, {
        component: styles.component,
        dimLine: styles.dimLine,
        bar: styles.bar,
        forkFill: styles.forkFill,
        frameFill: styles.frameFill,
        joint: styles.joint,
        tire: styles.tire,
        rim: styles.rim,
        text: styles.text
      })
    }}
  >
  </div>)
}
