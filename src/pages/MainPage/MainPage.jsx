import React, { useState, useEffect } from "react";
import { Responsive, WidthProvider } from "react-grid-layout";
import axios from "axios";
import { Cookies } from "react-cookie";
import Grid from "@mui/material/Grid";
import Divider from "@mui/material/Divider";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import Loader from "../../components/Loader/Loader";
import "../../../node_modules/react-grid-layout/css/styles.css";
import "../../../node_modules/react-resizable/css/styles.css";
import "./styles.css";
import { BiLeftArrow, BiRightArrow } from "react-icons/bi";
import { useNavigate } from "react-router-dom";
import AppConfig from "../../auth/config.js";
import { AiOutlineLogout } from "react-icons/ai";
import { handleLogout } from "../../utils/utils";
import AuthService from "../../auth/utils/authService";
import EnergyAnalytics from "../../components/EnergyAnalytics/EnergyAnalytics";
import ChatBot from "../../components/ChatBot/ChatBot";
import SmartWashroom from "../../components/Smart/SmartWashroom";
import Sustainability from "../../components/Sustainability/Sustainability";
import AirIndex1 from "../../components/AirIndex/AirIndex1";
import ResponsiveContainer from "../../components/AirIndex1/Render";
import { menuConfig } from "./menuConfig"; // Import the configuration
import ThemeToggleButton from "../../components/ThemeToggleButton";
import { useTheme } from "../../components/ThemeContext";
import Energy from "../../components/Energy/Energy";
import Sld from "../../components/Sld/Sld";

const ScreenLayout = WidthProvider(Responsive);

const authService = AuthService();

const cookies = new Cookies();

const MainPage = () => {
  const [deviceRowHeight, setDeviceRowHeight] = useState();

  const WEBAPPAPIURL = `${AppConfig.API_URL}/api/`;

  const accessToken = cookies.get("accessToken");

  const [globalTower, setGlobalTower] = useState(cookies.get("global_tower"));

  const [scrolling, setScrolling] = useState(false);

  const [openLogout, setOpenLogout] = useState(false);

  const [activeMenu, setActiveMenu] = useState("Sustainability");
  const { themes } = useTheme();

  const menus = [
    { name: "Sustainability", submenus: [] },
    { name: "Energy Analytics", submenus: [] },
    { name: "Energy Analytics(v1)", submenus: [] },
    { name: "Smart WashRoom", submenus: [] },
    { name: "AI Assist", submenus: [] },
    { name: "Indoor Air Quality1", submenus: [] },
    { name: "Indoor Air Quality", submenus: [] },
    { name: "Energy", submenus: [] },
  ].filter((menu) => menuConfig[menu.name.replace(/\s+/g, "")]); // Filter menus based on configuration

  const [isTimer, setTimer] = useState(false);

  const [userInfo, setUserInfo] = useState({
    loading: false,
    data: null,
    count: 0,
    err: null,
  });

  useEffect(() => {
    const handleScroll = () => {
      const navbar = document.getElementById("custom-navbar");
      const sticky = navbar.offsetTop;
      if (window.scrollY >= sticky) {
        setScrolling(true);
      } else {
        setScrolling(false);
      }
    };

    window.addEventListener("scroll", handleScroll);

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  function getUserInfo() {
    if (accessToken) {
      setUserInfo({
        loading: true,
        data: null,
        count: 0,
        err: null,
      });

      const config = {
        method: "get",
        url: `${WEBAPPAPIURL}v4/userinformation`,
        withCredentials: false,
        headers: {
          endpoint: window.localStorage.getItem("api-url"),
          Authorization: `Bearer ${accessToken}`,
        },
      };

      axios(config)
        .then((response) => {
          setUserInfo({
            loading: false,
            data: response.data.data,
            count: response.data.length,
            err: null,
          });
        })
        .catch((error) => {
          if (!isTimer) {
            setUserInfo({
              loading: false,
              data: null,
              count: 0,
              err: error,
            });
          }
        });
    }
  }

  function refreshToken() {
    const data = new FormData();
    const authData = authService.getCredentials();

    data.append("grant_type", "refresh_token");
    data.append("client_id", authData.client_id);
    data.append("client_secret", authData.client_secret);
    data.append("refresh_token", authService.getRefreshToken());

    const config = {
      method: "post",
      url: `${WEBAPPAPIURL}authentication/oauth2/token`,
      data,
      withCredentials: false,
      headers: { endpoint: window.localStorage.getItem("api-url") },
    };

    axios(config)
      .then((response) => {
        authService.setToken(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }
  const navigate = useNavigate();

  useEffect(() => {
    if (!accessToken) {
      refreshToken();
    }
  }, [accessToken]);

  useEffect(() => {
    getUserInfo();
  }, []);

  return (
    <>
      {userInfo && userInfo.loading && (
        <div className="">
          <Loader />
        </div>
      )}
      {userInfo &&
        !userInfo.loading &&
        userInfo.data &&
        (!userInfo.data.user_property ||
          (userInfo.data.user_property &&
            userInfo.data.user_property === "NOC")) && (
          <>
            <div
              className={`responsive-navbar ${
                scrolling ? "sticky" : "sticky"
              } ${themes === "light" ? "responsive-navbar-light" : ""}`}
              id="custom-navbar"
            >
              {menus &&
                menus.map((menu) => (
                  <a
                    key={menu.name}
                    style={{ cursor: "pointer" }}
                    className={`menu-item ${
                      activeMenu === menu.name ? "active" : ""
                    }`}
                    onClick={() => setActiveMenu(menu.name)}
                  >
                    {menu.name}
                    {menu.submenus.length > 0 && activeMenu === menu.name && (
                      <div className="submenu">
                        <div className="flex">
                          {menu.submenus.map((submenu, subIndex) => (
                            <React.Fragment key={subIndex}>
                              <div className="submenu-item">{submenu}</div>
                              {subIndex < menu.submenus.length - 1 && (
                                <Divider
                                  sx={{
                                    margin: "8px 0",
                                    borderColor: "white",
                                    borderWidth: "1px",
                                    width: "100%",
                                  }}
                                />
                              )}
                            </React.Fragment>
                          ))}
                        </div>
                      </div>
                    )}
                  </a>
                ))}
              <div className="logout-icon">
                <ThemeToggleButton />
                <AiOutlineLogout
                  size={20}
                  onClick={() => setOpenLogout(true)}
                  className={`pinned-icon arrow-icon ${
                    themes === "dark" ? "dark-arrow" : "light-arrow"
                  }`}
                />
              </div>
            </div>

            <div
              className={`content ${themes === "dark" ? "content-dark" : ""}`}
            >
              <Grid
                container
                spacing={0}
                columns={{ xs: 4, sm: 8, md: 12, lg: 12 }}
                className={`main-content ${
                  themes === "dark" ? "main-content-dark" : "main-content-light"
                }`}
              >
                <Grid item xs={12} sm={12} md={12} lg={12}>
                  {activeMenu === "Smart WashRoom" && <SmartWashroom />}
                  {activeMenu === "AI Assist" && <ChatBot />}
                  {activeMenu === "Energy Analytics(v1)" && <EnergyAnalytics />}
                  {activeMenu === "Sustainability" && <Sustainability />}
                  {activeMenu === "Indoor Air Quality1" && <AirIndex1 />}
                  {activeMenu === "Indoor Air Quality" && (
                    <ResponsiveContainer />
                  )}
                  {activeMenu === "Energy Analytics" && <Energy/>}
                  {activeMenu === "Energy" && <Sld/>}
                </Grid>
              </Grid>
              <Dialog
                open={openLogout}
                onClose={() => setOpenLogout(false)}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
              >
                <DialogTitle id="alert-dialog-title">{"Logout ?"}</DialogTitle>
                <DialogContent>
                  <DialogContentText id="alert-dialog-description">
                    Do you want to be logged out
                  </DialogContentText>
                </DialogContent>
                <DialogActions>
                  <Button onClick={() => setOpenLogout(false)}>Cancel</Button>
                  <Button onClick={handleLogout} autoFocus>
                    Logout
                  </Button>
                </DialogActions>
              </Dialog>
            </div>
          </>
        )}
      {userInfo &&
        !userInfo.loading &&
        userInfo.data &&
        userInfo.data.user_property &&
        userInfo.data.user_property === "Desktop" && (
          <div className="main-box">
            <ScreenLayout
              margin={[7, 8]}
              className="layout"
              breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
              cols={{ lg: 3, md: 3, sm: 2, xs: 2, xxs: 1 }}
              onBreakpointChange={(newBreakpoint) =>
                newBreakpoint === "xxs"
                  ? setDeviceRowHeight(200)
                  : newBreakpoint === "sm"
                  ? setDeviceRowHeight(250)
                  : setDeviceRowHeight(150)
              }
              rowHeight={deviceRowHeight}
            >
              <div key="a">
                <Sustainability />
              </div>
              <div key="b">
                <EnergyAnalytics />
              </div>
              <div key="c">
                <SmartWashroom />
              </div>
              <div key="d">
                <ChatBot />
              </div>
            </ScreenLayout>
            <div className="down">
              <GlobalFilter setGlobalTower={setGlobalTower} />
            </div>
            <div className="log-out-box" onClick={handleLogout}>
              <button className="arrow-btn">
                <AiOutlineLogout size={20} className="arrow-icon" />
              </button>
            </div>
            <div className="arrows-box">
              <button
                onClick={() => navigate("/operations")}
                className="arrow-btn"
              >
                <BiRightArrow size={20} className="arrow-icon" />
              </button>
            </div>
          </div>
        )}
    </>
  );
};

export default MainPage;
