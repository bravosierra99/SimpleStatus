import Status from "./Status";
import { useState } from "react";

import styles from "./StatusGrid.module.css";
function StatusGrid(props) {
  // function fetchStatuses() {
  //   const response = fetch("http://localhost:8001/components/statuses").then(response => {response.json()});
  //   return response;
  // }
  const [Statuses, setStatuses] = useState([])
  fetch(
    "http://localhost:8001/components/statuses"
  ).then((statuses) => {
    return statuses.json();
  }).then(data => {
    const StatusObjects = data.map(status => {return <Status {...status}/>});
    setStatuses(StatusObjects)});


  const statuses = props.statuses
    ? props.statuses.map((status) => <Status {...status} />)
    : Statuses;

  return <div className={styles.statusGrid}>{statuses}</div>;
}

export default StatusGrid;
