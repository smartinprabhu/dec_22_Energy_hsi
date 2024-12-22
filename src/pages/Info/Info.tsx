import React from "react";
import { AiOutlineLogout } from "react-icons/ai";
import { handleLogout } from "../../utils/utils";
import { useNavigate } from "react-router-dom";
import { BiRightArrow, BiLeftArrow } from "react-icons/bi";
import ESGOne from "../../components/ESGOne/ESGOne";
import Performance from "../../components/Performance/Performance";
import MaintenanceAlarm from "../../components/MaintenanceAlarm/MaintenanceAlarm";
import ESGTwo from "../../components/ESGTwo/ESGTwo";
import ESGThree from "../../components/ESGThree/ESGThree";
import PTwo from "../../components/PTwo/PTwo";
import SnackBar from "../../components/SnackBar/SnackBar";
import { Backdrop, CircularProgress } from "@mui/material";
import useMultipleUrlData from "../../hooks/apiHook";
import "./Info.css";

const Info: React.FC = () => {
  const navigate = useNavigate();

  const { data, isLoading, error } = useMultipleUrlData("htGrid");
  const { data: wData, isLoading: tankLoading } =
    useMultipleUrlData("getWaterTankValues");

  const { data: idata } = useMultipleUrlData("inspectionSummary");

  const pmTeamC = data?.data?.PmTeam?.compelete;
  const pmTeamM = data?.data?.PmTeam?.missed;
  const pmTeamU = data?.data?.PmTeam?.upcoming;

  const mAndEC = idata?.data?.mAndE?.compelete;
  const mAndEM = idata?.data?.mAndE?.missed;
  const mAndEU = idata?.data?.mAndE?.upcoming;

  const softServiceC = idata?.data?.softService?.compelete;
  const softServiceM = idata?.data?.softService?.missed;
  const softServiceU = idata?.data?.softService?.upcoming;

  const completed: any = parseInt(mAndEC) + parseInt(softServiceC);
  const missed: any = parseInt(mAndEM) + parseInt(softServiceM);
  const upcoming: any = parseInt(mAndEU) + parseInt(softServiceU);

  const completedPercentage =
    (completed / (completed + missed + upcoming)) * 100;

  const kWH = data?.data?.chartData?.incomerMeter.reduce(
    (n: any, { consumption }: any) => n + consumption,
    0
  );

  const consumptionSum = {};

  for (const tankDataKey in wData?.data?.chartData) {
    const tankData = wData?.data?.chartData[tankDataKey];

    for (const entry of tankData) {
      const date = entry?.date
        ? entry?.date?.split(" ")[0]
        : entry?.startDate?.split(" ")[0];
      const consumption = entry.consumption;

      if (consumptionSum[date]) {
        consumptionSum[date] += consumption;
      } else {
        consumptionSum[date] = consumption;
      }
    }
  }

  let consumptionArray = Object.values(consumptionSum);

  consumptionArray = consumptionArray.map((each: any) =>
    parseFloat(each.toFixed(2))
  );

  const sumOfArray: any = consumptionArray.reduce((a: any, c: any) => a + c, 0);
  return (
    <div className="info-main">
      <div className="info-category">
        <ESGOne />
        <Performance />
        <MaintenanceAlarm />
      </div>
      <div className="info-cat-info">
        <table
          style={{
            background: "#000000 0% 0% no-repeat padding-box",
            margin: 0,
            height: "33.3%",
          }}
          className="table-info"
        >
          <tr className="info-box-header b-b-none">
            <th className="info-card-title">G1</th>
            <th className="info-card-title">G2</th>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item">{kWH ? kWH : 0} kWh</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item">0 kWh</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon gauge-lable"></div>
                <p className="info-card-item">
                  {wData ? parseFloat(sumOfArray?.toFixed(2)) : 0} KL
                </p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon gauge-lable"></div>
                <p className="info-card-item">0 KL</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-green gauge-lable"></div>
                <p className="info-card-item">0 kg</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-green gauge-lable"></div>
                <p className="info-card-item">0 kg</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item">0 mt CO2eq</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item">0 mt CO2eq</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon gauge-lable"></div>
                <p className="info-card-item">0 incidents</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon gauge-lable"></div>
                <p className="info-card-item">0 incidents</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item">0 hr 30 min</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item">0 hr 0 min</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-green gauge-lable"></div>
                <p className="info-card-item">Good</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-green gauge-lable"></div>
                <p className="info-card-item">Good</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item">PM2.5: 0 μg/m³</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item">PM2.5: 0 μg/m³</p>
              </div>
            </td>
          </tr>
        </table>
        <table
          style={{
            background: "#000000 0% 0% no-repeat padding-box",
            margin: 0,
            height: "33.3%",
          }}
          className="table-info"
        >
          <tr className="info-box-header b-b-none bg-black">
            <th className="info-card-title title-invisible">G1</th>
            <th className="info-card-title light-bg"></th>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item">0%</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item ">0%</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon gauge-lable"></div>
                <p className="info-card-item">0 Hours</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon gauge-lable"></div>
                <p className="info-card-item">0 Hours</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-green gauge-lable"></div>
                <p className="info-card-item">0%</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-green gauge-lable"></div>
                <p className="info-card-item">0%</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item">₹ 0</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item">₹ 0</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon gauge-lable"></div>
                <p className="info-card-item">₹ 0</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon gauge-lable"></div>
                <p className="info-card-item">₹ 0</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-green gauge-lable"></div>
                <p className="info-card-item">₹ 0</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-green gauge-lable"></div>
                <p className="info-card-item">₹ 0</p>
              </div>
            </td>
          </tr>

          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item">₹ 0</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item">₹ 0</p>
              </div>
            </td>
          </tr>
        </table>
        <table
          style={{
            background: "#000000 0% 0% no-repeat padding-box",
            margin: 0,
            height: "33.3%",
          }}
          className="table-info"
        >
          <tr className="info-box-header b-b-none bg-black">
            <th className="info-card-title title-invisible">G1</th>
            <th className="info-card-title light-bg"></th>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item">
                  {completedPercentage ? completedPercentage.toFixed(2) : 0}%
                </p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item">0%</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon gauge-lable"></div>
                <p className="info-card-item">0 Hours</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon gauge-lable"></div>
                <p className="info-card-item">0 Hours</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-green gauge-lable"></div>
                <p className="info-card-item">0%</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-green gauge-lable"></div>
                <p className="info-card-item">0%</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item"> 0</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item"> 0</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon gauge-lable"></div>
                <p className="info-card-item"> 0</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon gauge-lable"></div>
                <p className="info-card-item"> 0</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-green gauge-lable"></div>
                <p className="info-card-item"> 0</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-green gauge-lable"></div>
                <p className="info-card-item"> 0</p>
              </div>
            </td>
          </tr>
          <tr className="b-b-none">
            <td className="info-card-item">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item"> 0</p>
              </div>
            </td>
            <td className="info-card-item light-bg">
              <div className="pie-chart-legend-box-inner">
                <div className="legend-icon-orange gauge-lable"></div>
                <p className="info-card-item"> 0</p>
              </div>
            </td>
          </tr>
        </table>
      </div>
      <div className="info-cat-info-next">
        <ESGTwo />
        <PTwo />
        <PTwo />
      </div>
      <div className="info-cat-info-next">
        <ESGThree />
        <PTwo />
        <PTwo />
      </div>
      <SnackBar error={error} />
      <Backdrop
        sx={{ color: "#fff", zIndex: (theme) => theme.zIndex.drawer + 1 }}
        open={isLoading || tankLoading}
        invisible
      >
        <CircularProgress color="primary" />
      </Backdrop>
      <div className="log-out-box" onClick={handleLogout}>
        <button className="arrow-btn">
          <AiOutlineLogout size={20} className="arrow-icon" />{" "}
        </button>
      </div>
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

export default Info;
