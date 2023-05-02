const successCallback = (position) => {
    console.log(position);
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
};
  
const errorCallback = (error) => {
    console.log(error);
};

const options = {
    enableHighAccuracy: true,
    timeout: 10000,
    maximumAge: 0
};
  

navigator.geolocation.getCurrentPosition(
  successCallback,
  errorCallback,
  options
);

// Track if users location changes
const id = navigator.geolocation.watchPosition(successCallback, errorCallback);

