import styles from "./Status.module.css";
import StatusDate from "./StatusDate";

function Status(props) {
  return (
    <div className={styles.status}>
      <h2>{props.name}</h2>
      <StatusDate date={props.date} />
    </div>
  );
}

export default Status;
