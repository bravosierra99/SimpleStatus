import styles from "./StatusDate.module.css";

function StatusDate(props) {
  const month = props.date.toLocaleString("en-US", { month: "long" });
  const day = props.date.toLocaleString("en-US", { day: "2-digit" });
  const year = props.date.getFullYear();
  const options = {hour: '2-digit', minute: '2-digit', hour12:false }
  const time = props.date.toLocaleTimeString("en-US", options);
//   const time = props.date.getHours() + ":" + props.date.getMinutes();
// let t  = new Date()
// t.format()

  return (
    <div className={styles.greenDate}>
      <div className={styles.time}>{time}</div>
      <div className={styles.date}>
        {day} {month} {year}
      </div>
    </div>
  );
}

export default StatusDate;
