import React from 'react';

export function getTotal(data) {
  let count = 0;
  if (data && data.length > 0) {
    for (let i = 0; i < data.length; i += 1) {
      if (data[i].ks_dashboard_item_type === 'ks_tile') {
        count += data[i].datasets[0];
      }
    }
  }
  return count;
}

export const getMaxLenghtForFields = () => {
    const maxLengthObj = {
      username: 50,
      password: 50,
      accountId: 10,
    };
    return maxLengthObj;
  };

  export function convertToUppercase(str) {
    let res = "";
    if (str) {
      res = str.toString().toUpperCase();
    }
    return res;
  }