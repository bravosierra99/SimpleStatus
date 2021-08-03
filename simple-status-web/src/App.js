import logo from "./logo.svg";
import "./App.css";
import StatusGrid from "./components/Status/StatusGrid";

const today = new Date();
const yesterday = new Date(today);

// const today = "today";
// const yesterday = "yesterday";

yesterday.setDate(yesterday.getDate() - 1);
const DUMMY_STATUSES = [
  { name: "component1", date: today, status: "Green", key: "comp1" },
  {
    name: "component2",
    date: today,
    status: "Green",
    key: "comp2",
  },
];

console.log(DUMMY_STATUSES);

function App() {
  return (
    <div>
      <h2>Simple Status Server</h2>
      <StatusGrid statuses={DUMMY_STATUSES} />
    </div>
  );
}

export default App;
