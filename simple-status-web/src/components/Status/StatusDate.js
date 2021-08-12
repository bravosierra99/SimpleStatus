import styles from "./StatusDate.module.css";
import Popup from "reactjs-popup";
import 'reactjs-popup/dist/index.css';
import './Popup.css';
import { useState } from "react";

function StatusDate(props) {
  const month = props.date.toLocaleString("en-US", { month: "long" });
  const day = props.date.toLocaleString("en-US", { day: "2-digit" });
  const year = props.date.getFullYear();
  const options = { hour: "2-digit", minute: "2-digit", hour12: false };
  const time = props.date.toLocaleTimeString("en-US", options);
  //   const time = props.date.getHours() + ":" + props.date.getMinutes();
  // let t  = new Date()
  // t.format()

  const [open, setOpen] = useState(false);
  const closeModal = () => setOpen(false);
  console.log(props.statusMessage)

  return (
    <div>
      <div
        onClick={() => setOpen((o) => !o)}
        className={styles.statusDate}
        style={{ backgroundColor: props.color }}
      >
        <div className={styles.time}>{time}</div>
        <div className={styles.date}>
          {day} {month} {year}
        </div>
      </div>
      <Popup open={open} closeOnDocumentClick onClose={closeModal}>
        <div className="modal">
          {/* <a className={styles.close} onClick={closeModal}>
            &times;
          </a> */}
          {props.statusMessage}
        </div>
      </Popup>
    </div>
  );
}

export default StatusDate;
