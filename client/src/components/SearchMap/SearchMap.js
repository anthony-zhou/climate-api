import Map from "../Map";
import {Search} from '../Search';
import styles from '../../../styles/Home.module.css';
import { useState } from "react";
import { DataWidget } from "./DataWidget";

const DEFAULT_CENTER = [38.907132, -77.036546]

const SearchMap = (props) => {

  const [climateData, setClimateData] = useState(null);
  const [address, setAddress] = useState('');
  const [latLng, setLatLng] = useState(DEFAULT_CENTER);

  const updateScreen = (data, address) => {
    const { year_1, year_2 } = data;
    setClimateData({
      year_1, year_2, address
    });
  }

  const handleSubmit = (address) => {
    const apiUrl = process.env.NEXT_ENV == 'production' ?
      'https://climate-heat-map.herokuapp.com' : 'http://127.0.0.1:5000';

    const url = apiUrl + '/data?address=' + encodeURIComponent(address);
    console.log(url);
    fetch(url)
      .then(res => res.json())
      .then(data => {
        updateScreen(data)
        setAddress(address)
        setLatLng([data.location['latitude'], data.location['longitude']]);
      });
  }

  return (<>
  <Search onSubmit={handleSubmit} />
  <DataWidget data={climateData} />
  <Map key={latLng} className={styles.homeMap} center={latLng} zoom={12}>
          {({ TileLayer, Marker, Popup }) => (
            <>
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution="&copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
              />
              <Marker position={latLng}>
                <Popup>
                  {address}
                </Popup>
              </Marker>
            </>
          )}
        </Map>
  </>)
}

export default SearchMap;
