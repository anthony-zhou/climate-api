import Head from 'next/head';

import Map from '../components/Map';
import {SearchMap} from '../components/SearchMap';
import styles from '../../styles/Home.module.css';


export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>Climate Heat Map</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Climate Heat Map
        </h1>

        <p className={styles.description}>
          Enter a street address to see heat projections for that area. 
        </p>

        <SearchMap>

        </SearchMap>
      </main>
      <footer className={styles.footer}>
        <p>
          Data from the <a href="https://interactive-atlas.ipcc.ch/">IPCC Interactive Atlas</a>. 
          Note that this is an oversimplified simulation, which only shows data from the 6th assessment report's SSP-5 8.5 scenario.
          Also note that data is aggregated across regions, meaning for example that the estimates for locations across Western North America will be the same. 
          Clearly this is not accurate to reality, but will not be until we get better spatial resolution on these publicly available APIs. 
        </p>
      </footer>
    </div>
  )
}
