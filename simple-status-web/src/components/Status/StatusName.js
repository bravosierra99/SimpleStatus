import React from "react";
import styles from "./StatusName.module.css";
import Popup from "reactjs-popup";
import { useState } from "react";

function StatusName(props) {
  const [open, setOpen] = useState(false);
  const closeModal = () => setOpen(false);

  return (
    <u>
      <h2 className={styles.name} onClick={() => setOpen((o) => !o)}>{props.name}</h2>
      <Popup open={open} closeOnDocumentClick onClose={closeModal}>
        <div className="modal">{props.details}</div>
      </Popup>
    </u>
  );
}

export default StatusName;
