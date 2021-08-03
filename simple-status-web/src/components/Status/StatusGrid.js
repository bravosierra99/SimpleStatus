import Status from "./Status";

import styles from './StatusGrid.module.css'
function StatusGrid(props) {
  return (
    <div className={styles.statusGrid}>
      {props.statuses.map((status) => (
        <Status {...status} />
      ))}
    </div>
  );
}

export default StatusGrid;
