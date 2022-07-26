export const DataWidget = (props) => {
  return (!props.data
    ? <></>
    : <div>
        <h2>{props.data.address}</h2>
        <h4>Mean days above 35°C/95°F in {props.data.year_1.year}: {props.data.year_1.ssp585}</h4>
        <h4>Mean days above 35°C/95°F in {props.data.year_2.year}: {props.data.year_2.ssp585}</h4>
    </div>);
}