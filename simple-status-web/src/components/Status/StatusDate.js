import styles from "./StatusDate.module.css";
import Popup from "reactjs-popup";
import "reactjs-popup/dist/index.css";
import "./Popup.css";
import { useState } from "react";

function time_values(date) {
  const month = date.toLocaleString("en-US", { month: "long" });
  const day = date.toLocaleString("en-US", { day: "2-digit" });
  const year = date.getFullYear();
  const options = { hour: "2-digit", minute: "2-digit", hour12: false };
  const time = date.toLocaleTimeString("en-US", options);
  return { month, day, year, options, time };
}

function timed_out(date, timeout) {
  const today = new Date();
  console.log(today + " " + date);
  const diff = Math.abs(today - date) / (1000 * 60);
  console.log(diff + " " + timeout);
  return diff > timeout;
}

function StatusDate(props) {
  const { month, day, year, options, time } = time_values(props.date);

  const [open, setOpen] = useState(false);
  const closeModal = () => setOpen(false);
  const timed_out_result = timed_out(props.date, props.config.timeout_min);
  const color =
    timed_out_result && props.color === "green"
      ? props.config.timeout_color
      : props.color;
  const timed_out_message = timed_out_result ? (
    <div>
      <br />
      <div>Status has Timed Out</div>
    </div>
  ) : (
    ""
  );

  return (
    <div>
      <div
        onClick={() => setOpen((o) => !o)}
        className={styles.statusDate}
        style={{ backgroundColor: color }}
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
          {timed_out_message}
        </div>
      </Popup>
    </div>
  );
}

export default StatusDate;
