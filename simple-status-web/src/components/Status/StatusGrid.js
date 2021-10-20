import Status from "./Status";
import { useState, useEffect } from "react";

import styles from "./StatusGrid.module.css";
function StatusGrid(props) {
  // function fetchStatuses() {
  //   const response = fetch("http://localhost:8001/components/statuses").then(response => {response.json()});
  //   return response;
  // }

  useEffect(() => {
    const interval = setInterval(() => {
    fetch("http://localhost/api/components/statuses")
      .then((statuses) => {
        return statuses.json();
      })
      .then((data) => {
        let StatusObjects = data.map((status) => {
          return <Status {...status} />;
        });
        if (StatusObjects.length === 0) {
          StatusObjects = <h3>No Statuses have been submitted yet</h3>;
        }

        setStatuses(StatusObjects);
      });
    },5000);
    return () => clearInterval(interval);
  }, []);
  const [Statuses, setStatuses] = useState(
    <h3>
      Fetching Data from Server, This message should only be up momentarily. In
      fact if you are reading this something probably wrong
    </h3>
  );

  const statuses = props.statuses
    ? props.statuses.map((status) => <Status {...status} />)
    : Statuses;

  return <div className={styles.statusGrid}>{statuses}</div>;
}

export default StatusGrid;
