import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Cookies } from 'react-cookie';

import MainPage from "./pages/MainPage/MainPage";
import AccountLogin from "./auth/accountIdLogin";
import "./app.scss";

const cookies = new Cookies();

function App() {
 
  const isLoggedIn = cookies.get('accessToken');

  return (
  
    <>
    {isLoggedIn && (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainPage />} />
      </Routes>
    </BrowserRouter>
    )}
     {!isLoggedIn && (
     <BrowserRouter>
      <Routes>
          <Route path="*" element={<AccountLogin />} />
      </Routes>
    </BrowserRouter>
   )}
   </>
  );
}

export default App;
