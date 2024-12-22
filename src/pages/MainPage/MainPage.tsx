import { Responsive, WidthProvider } from "react-grid-layout";
import { Cookies } from 'react-cookie';

import "../../../node_modules/react-grid-layout/css/styles.css";
import "../../../node_modules/react-resizable/css/styles.css";
import "./styles.css";
import { BiLeftArrow, BiRightArrow } from "react-icons/bi";
import EnergyAnalytics from "../../components/EnergyAnalytics/EnergyAnalytics";
import Sustainability from "../../components/Sustainability/Sustainability";
import SmartWashroom from "../../components/Smart/SmartWashroom";
import ChatBot from "../../components/ChatBot/ChatBot";

const ScreenLayout = WidthProvider(Responsive);

const MainPage = () => {
  return (
    <div className="main-box">
      <ScreenLayout
        margin={[10, 5.05]}
        className="layout"
        layouts={{
          lg: energyLayout,
          md: energyLayout,
          sm: energyLayout,
          xs: energyLayout,
          xxs: energyLayout,
        }}
        breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
        cols={{ lg: 3, md: 3, sm: 3, xs: 3, xxs: 3 }}
        // rowHeight={2.65}
        onLayoutChange={(layouts) => handleLayoutChange(layouts)}
      >
        <div key="a">
          <Sustainability/>
        </div>
        <div key="b">
        <EnergyAnalytics/>
        </div>
        <div key="c">
          <SmartWashroom/>
        </div>
        <div key="d">
          <ChatBot/>
        </div>
      </ScreenLayout>
      <div className="arrows-box">
        <button onClick={() => navigate("/")} className="arrow-btn">
          <BiLeftArrow size={20} className="arrow-icon" />{" "}
        </button>
        <button onClick={() => navigate("/operations")} className="arrow-btn">
          <BiRightArrow size={20} className="arrow-icon" />{" "}
        </button>
      </div>
    </div>
  );
};

export default MainPage;
