import React, { useState, useCallback, useEffect } from "react";
import ReactFlow, {
  ReactFlowProvider,
  addEdge,
  Background,
  applyNodeChanges,
  applyEdgeChanges,
  Controls,
} from "react-flow-renderer";
import CustomNode from "./CustomNode";
import "./Flow.css";
import Energy from "../Energy/Energy";
import Sustainability from "../Sustainability/Sustainability";
import { useTheme } from "../ThemeContext";
import CardHeader from "../CardHeader/card1";

const GroupNode = ({ data }) => {
  const { children = [] } = data || {}; // Use empty array as fallback

  return (
    <div style={{ border: "1px solid black", padding: "10px" }}>
      <div>
        {children.length > 0 ? (
          children.map((child) => (
            <div key={child.id}>
              {/* Render your child node here */}
              {child.data?.text || "No text available"}{" "}
              {/* Fallback for child text */}
            </div>
          ))
        ) : (
          <p>No child nodes available.</p>
        )}
      </div>
    </div>
  );
};

const nodeTypes = {
  custom: CustomNode,
  group: GroupNode,
};
const initialNodes = [
  {
    width: 151,
    height: 81,
    id: "1",
    type: "custom",
    data: {
      text: "Dallas Tower",
      imageUrl:
        "https://res.cloudinary.com/dp6envw5o/image/upload/v1678345927/Group_29506_cdgdk8.svg",
      handlers: [
        {
          handle: {
            type: "source",
            handleId: "a",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 10,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 287.32480000000004,
      y: -190.33311999999995,
    },
    selected: false,
    positionAbsolute: {
      x: 287.32480000000004,
      y: -190.33311999999995,
    },
    dragging: false,
  },
  {
    id: "5",
    type: "custom",
    mete: "energy",
    data: {
      text: "I/C From Meter Cubical",
      status: "active",
      imageUrl:
        "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
      energyMeter: {
        id: "68B6B341A848-7",
      },
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "c",
            position: "left",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "d",
            position: "right",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 286.9014470343305,
      y: -53.00836005974684,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 286.9014470343305,
      y: -53.00836005974684,
    },
    dragging: false,
  },
  {
    id: "6",
    type: "custom",
    mete: "energy",
    data: {
      text: "O/G Transformer 01",
      status: "inactive",
      imageUrl:
        "https://res.cloudinary.com/dujhloknt/image/upload/v1733395030/transformer_mlhadr.png",
      id: "198",
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 1.1295610160854466,
      y: 76.7420388034057,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 1.1295610160854466,
      y: 76.7420388034057,
    },
    dragging: false,
  },
  {
    width: 151,
    height: 81,
    id: "7",
    type: "custom",
    data: {
      text: "O/G Transformer 02",
      status: "active",
      imageUrl:
        "https://res.cloudinary.com/dujhloknt/image/upload/v1733395030/transformer_mlhadr.png",
      id: "197",
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 288.49274393446285,
      y: 75.63583381288211,
    },
    selected: false,
    positionAbsolute: {
      x: 288.49274393446285,
      y: 75.63583381288211,
    },
    dragging: false,
  },
  {
    id: "8",
    type: "custom",
    mete: "energy",
    data: {
      text: "O/G Transformer 03",
      status: "not",
      imageUrl:
        "https://res.cloudinary.com/dujhloknt/image/upload/v1733395030/transformer_mlhadr.png",
      id: "196",
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 597.4694042082085,
      y: 71.92609952091408,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 597.4694042082085,
      y: 71.92609952091408,
    },
    dragging: false,
  },
  {
    width: 151,
    height: 81,
    id: "9",
    type: "custom",
    mete: "energy",
    data: {
      text: "O/G Transformer 04",
      status: "active",
      imageUrl:
        "https://res.cloudinary.com/dujhloknt/image/upload/v1733395030/transformer_mlhadr.png",
      id: "197",
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 833.8731668498693,
      y: 70.843171903311,
    },
    selected: true,
    positionAbsolute: {
      x: 833.8731668498693,
      y: 70.843171903311,
    },
    dragging: false,
  },
  {
    id: "10",
    type: "custom",
    mete: "energy",
    data: {
      text: "LT KIOSK-03",
      status: "active",
      imageUrl:
        "https://res.cloudinary.com/dujhloknt/image/upload/v1733829925/Panel_dzvgsn.png",
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 0.7024999187805747,
      y: 324.23226374871524,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 0.7024999187805747,
      y: 324.23226374871524,
    },
    dragging: false,
  },
  {
    id: "11",
    type: "custom",
    mete: "energy",
    data: {
      text: "LT KIOSK-02",
      status: "inactive",
      imageUrl:
        "https://res.cloudinary.com/dujhloknt/image/upload/v1733829925/Panel_dzvgsn.png",
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 291.2722370227871,
      y: 312.975801075376,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 291.2722370227871,
      y: 312.975801075376,
    },
    dragging: false,
  },
  {
    id: "12",
    type: "custom",
    mete: "energy",
    data: {
      text: "LT KIOSK-01",
      status: "inactive",
      imageUrl:
        "https://res.cloudinary.com/dujhloknt/image/upload/v1733829925/Panel_dzvgsn.png",
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        textAlign: "center",
        alignItems: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 604.8001047505506,
      y: 307.8160463651299,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 604.8001047505506,
      y: 307.8160463651299,
    },
    dragging: false,
  },
  {
    id: "13",
    type: "custom",
    mete: "energy",
    data: {
      text: "LT KIOSK-04",
      status: "active",
      imageUrl:
        "https://res.cloudinary.com/dujhloknt/image/upload/v1733829925/Panel_dzvgsn.png",
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 834.6513721706813,
      y: 304.921739413772,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 834.6513721706813,
      y: 304.921739413772,
    },
    dragging: false,
  },
  {
    id: "14",
    type: "custom",
    mete: "energy",
    data: {
      text: "Transformer-OG-3",
      imageUrl:
        "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
      energyMeter: {
        id: "68B6B341A848-6",
      },
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 0.6242756852000326,
      y: 198.17928724337708,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 0.6242756852000326,
      y: 198.17928724337708,
    },
    dragging: false,
  },
  {
    id: "15",
    type: "custom",
    mete: "energy",
    data: {
      text: "Transformer-OG-2",
      status: "not",
      imageUrl:
        "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
      energyMeter: {
        id: "68B6B341A848-5",
      },
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 288.278968235025,
      y: 189.98963651703468,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 288.278968235025,
      y: 189.98963651703468,
    },
    dragging: false,
  },
  {
    id: "16",
    type: "custom",
    mete: "energy",
    data: {
      text: "Transformer-OG-1",
      imageUrl:
        "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
      energyMeter: {
        id: "68B6B341A848-4",
      },
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 599.3889361940046,
      y: 183.93657688417767,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 599.3889361940046,
      y: 183.93657688417767,
    },
    dragging: false,
  },
  {
    id: "17",
    type: "custom",
    mete: "energy",
    data: {
      text: "Transformer-OG-4",
      imageUrl:
        "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
      energyMeter: {
        id: "68B6B341A848-3",
      },
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 833.7813564017605,
      y: 184.47953481999866,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 833.7813564017605,
      y: 184.47953481999866,
    },
    dragging: false,
  },
  {
    id: "18",
    type: "custom",
    mete: "energy",
    data: {
      text: "Existing DRUPS -3 1600KVA",
      imageUrl:
        "https://res.cloudinary.com/dujhloknt/image/upload/v1733829960/DRUPS_kcmvwu.png",
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "right",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 0.17541402317931443,
      y: 451.0655503224864,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 0.17541402317931443,
      y: 451.0655503224864,
    },
    dragging: false,
  },
  {
    id: "19",
    type: "custom",
    mete: "energy",
    data: {
      text: "Existing DRUPS -2 1600KVA",
      imageUrl:
        "https://res.cloudinary.com/dujhloknt/image/upload/v1733829960/DRUPS_kcmvwu.png",
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "left",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 289.8605252165319,
      y: 445.9464140677326,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 289.8605252165319,
      y: 445.9464140677326,
    },
    dragging: false,
  },
  {
    id: "20",
    type: "custom",
    mete: "energy",
    data: {
      text: "DeRUPS STANDBY PANEL LOC:ELECTRICAL ROOM MD: KW",
      imageUrl:
        "https://res.cloudinary.com/dujhloknt/image/upload/v1733829960/DRUPS_kcmvwu.png",
      handlers: [
        {
          handle: {
            type: "source",
            handleId: "a",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 120,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 511.3214384914228,
      y: 410.4155798802305,
    },
    width: 151,
    height: 121,
    selected: false,
    positionAbsolute: {
      x: 511.3214384914228,
      y: 410.4155798802305,
    },
    dragging: false,
  },
  {
    id: "21",
    type: "custom",
    mete: "energy",
    data: {
      text: "BUS BAR",
      imageUrl:
        "https://res.cloudinary.com/dujhloknt/image/upload/v1733829925/BusBar_judesm.png",
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "target",
            handleId: "b",
            position: "left",
          },
        },
        {
          handle: {
            type: "target",
            handleId: "c",
            position: "right",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "d",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 650,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 167.26804143183492,
      y: 570.7448281169882,
    },
    width: 651,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 167.26804143183492,
      y: 570.7448281169882,
    },
    dragging: false,
  },
  {
    id: "22",
    type: "custom",
    mete: "energy",
    data: {
      text: "1X1600 KVA, 415V AC 50HZ DRUPS",
      status: "not",
      imageUrl:
        "https://res.cloudinary.com/dujhloknt/image/upload/v1733829960/DRUPS_kcmvwu.png",
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
        {
          handle: {
            type: "target",
            handleId: "c",
            position: "right",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 834.0291210111088,
      y: 437.37378981527837,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 834.0291210111088,
      y: 437.37378981527837,
    },
    dragging: false,
  },
  {
    id: "23",
    type: "custom",
    mete: "energy",
    data: {
      text: "DG-SET 2250KVS",
      imageUrl:
        "https://res.cloudinary.com/dujhloknt/image/upload/v1733839407/DG_hhnkq5.png",
      handlers: [
        {
          handle: {
            type: "source",
            handleId: "a",
            position: "left",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 1104.212168478706,
      y: 435.1762952606756,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 1104.212168478706,
      y: 435.1762952606756,
    },
    dragging: false,
  },
  {
    id: "24",
    type: "custom",
    mete: "energy",
    data: {
      text: "LT Panel 02 I/C from MAIN PDP PANEL (2F2)",
      imageUrl:
        "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
      energyMeter: {
        id: "68B6B341A86C-16",
      },
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        textAlign: "center",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 14.743093069783697,
      y: 691.6000043358963,
    },
    width: 151,
    height: 101,
    selected: false,
    positionAbsolute: {
      x: 14.743093069783697,
      y: 691.6000043358963,
    },
    dragging: false,
  },
  {
    id: "25",
    type: "custom",
    mete: "energy",
    data: {
      text: "LT Panel 02 I/C FROM 1750 KVA DG PANEL FDR NO:3",
      imageUrl:
        "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
      energyMeter: {
        id: "68B6B341A86C-32",
      },
      handlers: [
        {
          handle: {
            type: "source",
            handleId: "a",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        textAlign: "center",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: -194.6408616697212,
      y: 696.2168565810574,
    },
    width: 151,
    height: 101,
    selected: false,
    positionAbsolute: {
      x: -194.6408616697212,
      y: 696.2168565810574,
    },
    dragging: false,
  },
  {
    id: "26",
    type: "custom",
    mete: "energy",
    data: {
      text: "LT Panel 03 I/C FROM TRANSFORMER 3",
      imageUrl:
        "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
      energyMeter: {
        id: "68B6B341A81C-1",
      },
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        textAlign: "center",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 260.1549642312699,
      y: 687.5366101015294,
    },
    width: 151,
    height: 101,
    selected: false,
    positionAbsolute: {
      x: 260.1549642312699,
      y: 687.5366101015294,
    },
    dragging: false,
  },
  {
    id: "27",
    type: "custom",
    mete: "energy",
    data: {
      text: "LT Panel 03 F39 DB-33-CTD TERRACE",
      imageUrl:
        "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
      energyMeter: {
        id: "68B6B341A81C-14",
      },
      handlers: [
        {
          handle: {
            type: "source",
            handleId: "a",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        textAlign: "center",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 438.08125770162343,
      y: 687.6979091141831,
    },
    width: 151,
    height: 101,
    selected: false,
    positionAbsolute: {
      x: 438.08125770162343,
      y: 687.6979091141831,
    },
    dragging: false,
  },
  {
    id: "28",
    type: "custom",
    mete: "energy",
    data: {
      text: "LT Panel 04 8F2-IC 02 From Drups 2 & 3",
      imageUrl:
        "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
      energyMeter: {
        id: "68B6B341A81C-16",
      },
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        textAlign: "center",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 655.5526326180933,
      y: 682.8729532382242,
    },
    width: 151,
    height: 101,
    selected: false,
    positionAbsolute: {
      x: 655.5526326180933,
      y: 682.8729532382242,
    },
    dragging: false,
  },
  {
    id: "29",
    type: "custom",
    mete: "energy",
    data: {
      text: "LT Panel 04 IC FROM 1750 KVA DG PANEL FDR NO:3",
      imageUrl:
        "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
      energyMeter: {
        id: "68B6B341A81C-29",
      },
      handlers: [
        {
          handle: {
            type: "source",
            handleId: "a",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 840.5419357282128,
      y: 677.7647786584819,
    },
    width: 151,
    height: 101,
    selected: false,
    positionAbsolute: {
      x: 840.5419357282128,
      y: 677.7647786584819,
    },
    dragging: false,
  },
  {
    id: "30",
    type: "custom",
    mete: "energy",
    data: {
      text: "IC From Drups 2 & 3",
      imageUrl:
        "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
      energyMeter: {
        id: "68B6B341A858-13",
      },
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 1095.5375000559804,
      y: 685.3334871093408,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 1095.5375000559804,
      y: 685.3334871093408,
    },
    dragging: false,
  },
  {
    id: "31",
    type: "custom",
    mete: "energy",
    data: {
      text: "IC Panel 01 lighting ATS panel",
      imageUrl:
        "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
      energyMeter: {
        id: "68B6B341A858-11",
      },
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 1257.0619823327706,
      y: 683.746443576837,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 1257.0619823327706,
      y: 683.746443576837,
    },
    dragging: false,
  },
  {
    id: "32",
    type: "custom",
    mete: "energy",
    data: {
      text: "IC Panel 02 lighting ATS panel",
      imageUrl:
        "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
      energyMeter: {
        id: "68B6B341A858-12",
      },
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 1430.075622814376,
      y: 687.342721385949,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 1430.075622814376,
      y: 687.342721385949,
    },
    dragging: false,
  },
  {
    id: "33",
    type: "custom",
    mete: "energy",
    data: {
      text: "DG-SEt-01 5000KVA 415V",
      imageUrl:
        "https://res.cloudinary.com/dujhloknt/image/upload/v1733839407/DG_hhnkq5.png",
      handlers: [
        {
          handle: {
            type: "source",
            handleId: "a",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 1625.4916356915103,
      y: 686.9241214388396,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 1625.4916356915103,
      y: 686.9241214388396,
    },
    dragging: false,
  },
  {
    id: "34",
    type: "custom",
    mete: "energy",
    data: {
      text: "LT Panel 05 I/C",
      imageUrl:
        "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
      energyMeter: {
        id: "68B6B341A858-17",
      },
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 1865.738972791356,
      y: 678.1137919739754,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 1865.738972791356,
      y: 678.1137919739754,
    },
    dragging: false,
  },
  {
    id: "35",
    type: "custom",
    mete: "energy",
    data: {
      text: "IC from De-Rups 04",
      imageUrl:
        "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
      energyMeter: {
        id: "68B6B341AC88-1",
      },
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 2026.9402865345444,
      y: 676.8606383475715,
    },
    width: 151,
    height: 81,
    selected: false,
    positionAbsolute: {
      x: 2026.9402865345444,
      y: 676.8606383475715,
    },
    dragging: false,
  },
  {
    id: "36",
    type: "custom",
    mete: "energy",
    data: {
      text: "LT Panel 01 - Incomer 01 From DRUPS 1",
      imageUrl:
        "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
      energyMeter: {
        id: "68B6B341A86C-1",
      },
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "left",
          },
        },
        {
          handle: {
            type: "source",
            handleId: "b",
            position: "bottom",
          },
        },
      ],
      style: {
        width: 150,
        height: 100,
        borderRadius: 8,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        textAlign: "center",
        flexDirection: "column",
      },
    },
    position: {
      x: 2278.098969514992,
      y: 605.0087799163653,
    },
    width: 151,
    height: 101,
    selected: false,
    positionAbsolute: {
      x: 2278.098969514992,
      y: 605.0087799163653,
    },
    dragging: false,
  },
  {
    width: 471,
    height: 523,
    id: "37",
    type: "custom",
    mete: "energy",
    data: {
      text: "PANEL 01",
      description: true,
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
      ],
      style: {
        width: 450,
        height: "auto",
        borderRadius: 8,
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "space-between",
        alignItems: "center",
        textAlign: "center",
        padding: "10px",
      },
      energyMeters: [
        {
          text: "LT Panel 01 - F1-DB-21-NEW IMP",
          status: "active",
          id: "68B6B341A86C-2",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 01 - F2-DB-14-VAMANA",
          status: "inactive",
          id: "68B6B341A86C-3",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 01 - F3-DB-22-TLF CLEAN ROOM",
          status: "active",
          id: "68B6B341A86C-4",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 01 - F4-DB-09-TLF AREA",
          status: "active",
          id: "68B6B341A86C-5",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 01 - F5-DB-04-OLD IMP",
          status: "inactive",
          id: "68B6B341A86C-6",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 01 - F6-DB-28 & 28A-MPP",
          id: "68B6B341A86C-7",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 01 - F7-DB-02-OLD MPP",
          id: "68B6B341A86C-8",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 01 - F8 DB-32-VAMANA",
          id: "68B6B341A86C-9",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 01 - F9-DB-03-OLD IMP",
          id: "68B6B341A86C-10",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 01 - F10-DB-20-NEW IMP",
          id: "68B6B341A86C-11",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 01 - F11-MLDB-LT ROOM",
          id: "68B6B341A86C-12",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 01 - F12-DB-19-MIS",
          id: "68B6B341A86C-13",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 01 - F13-DB-45/PDB-569-LT ROOM/CHILLER YARD",
          id: "68B6B341A86C-14",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 01 - F14-PDB-153 & MCCB PANEL",
          id: "68B6B341A86C-15",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
      ],
    },
    position: {
      x: 2278.5826492935653,
      y: 885.9004598898941,
    },
    selected: false,
    dragging: false,
  },
  {
    width: 471,
    height: 379,
    id: "38",
    type: "custom",
    mete: "energy",
    data: {
      text: "PANEL 05",
      description: true,
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
      ],
      style: {
        width: 450,
        height: "auto",
        borderRadius: 8,
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "space-between",
        alignItems: "center",
        textAlign: "center",
        padding: "10px",
      },
      energyMeters: [
        {
          text: "LT Panel 05 2F1 DB-30 ACB OG 1000A",
          id: "68B6B341A858-18",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 05 3F1 Compressor",
          id: "68B6B341A858-20",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 05 3F2 Capacitors",
          id: "68B6B341A858-21",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 05 4F1 Bus Coupler OG-1",
          id: "68B6B341A858-22",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 05 4F2 Bus Coupler OG-2",
          id: "68B6B341A858-23",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 05 6F1 Bus Coupler OG-3",
          id: "68B6B341A858-24",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 05 6F2 DG DB 46",
          id: "68B6B341A858-25",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 05 7F1 DG OG4",
          id: "68B6B341A858-26",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 05 7F2 210 HP Air Compressor",
          id: "68B6B341A858-27",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 05 8F1 OG3",
          id: "68B6B341A858-28",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 05 8F2 OG4",
          id: "68B6B341A858-29",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "I/C From Erups Stand by PN FDR No 06",
          id: "68B6B341A858-30",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
      ],
    },
    position: {
      x: 1780.4131231187387,
      y: 890.05022281888,
    },
    selected: false,
    dragging: false,
  },
  {
    width: 471,
    height: 147,
    id: "39",
    type: "custom",
    mete: "energy",
    data: {
      text: "ATS PANEL",
      description: true,
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
      ],
      style: {
        width: 450,
        height: "auto",
        borderRadius: 8,
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "space-between",
        alignItems: "center",
        textAlign: "center",
        padding: "10px",
      },
      energyMeters: [
        {
          text: "LT Panel 04 F04, DB-06 & DB 177",
          id: "68B6B341A858-7",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 04 F03 DB 17 Basement Entrance",
          id: "68B6B341A858-8",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 04 F02 DB 12 Rest Room",
          id: "68B6B341A858-9",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel Spare",
          id: "68B6B341A858-10",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
      ],
    },
    position: {
      x: 1232.648849608268,
      y: 894.3776816284958,
    },
    selected: false,
    dragging: false,
  },
  {
    id: "40",
    type: "custom",
    mete: "energy",
    data: {
      text: "PANEL 04",
      description: true,
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
      ],
      style: {
        width: 450,
        height: "auto",
        borderRadius: 8,
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "space-between",
        alignItems: "center",
        textAlign: "center",
        padding: "10px",
      },
      energyMeters: [
        {
          text: "LT Panel 04 7F2-DB 39-Wedge Area",
          id: "68B6B341A81C-17",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 04 6F3-Nitrogen Plant",
          id: "68B6B341A81C-18",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 04 6F2-DB-SPARE",
          id: "68B6B341A81C-19",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 04 6F1-DB 40-1ST FLOOR HVT",
          id: "68B6B341A81C-20",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 04 5F3-DB-41-NEW HVT",
          id: "68B6B341A81C-21",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 04 4F3-DB-44-NEW IMP",
          id: "68B6B341A81C-22",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 04 4F2-DB-43-MOONSHINE SHOP",
          id: "68B6B341A81C-23",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 04 4F1-DEGASIFIER",
          id: "68B6B341A81C-24",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 04 3F3-DB-36-GLASS SHOP AHU",
          id: "68B6B341A81C-25",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 04 3F2-DB-35-SMART CATHODE",
          id: "68B6B341A81C-26",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 04 3F1-DB-47",
          id: "68B6B341A81C-27",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 04 2F2-DB-34-Wedge Area",
          id: "68B6B341A81C-28",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
      ],
    },
    position: {
      x: 747.5421840827802,
      y: 893.7457821345927,
    },
    width: 471,
    height: 398,
    selected: false,
    dragging: false,
  },
  {
    id: "41",
    type: "custom",
    mete: "energy",
    data: {
      text: "PANEL 03",
      description: true,
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
      ],
      style: {
        width: 450,
        height: "auto",
        borderRadius: 8,
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "space-between",
        alignItems: "center",
        textAlign: "center",
        padding: "10px",
      },
      energyMeters: [
        {
          text: "LT Panel 03 SPARE",
          id: "68B6B341A81C-2",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 03 F29 DB- SPARE",
          id: "68B6B341A81C-3",
          status: "not",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 03 F30 DB-29-SMART CATHODE",
          id: "68B6B341A81C-4",
          status: "active",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 03 F31 DB-27-NEW TP AREA",
          id: "68B6B341A81C-5",
          status: "inactive",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 03 F32 DB-37-WEDGE AREA",
          id: "68B6B341A81C-6",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 03 F33 DB-38-WEDGE AREA",
          id: "68B6B341A81C-7",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 03 F34 DB-26-A-ROOM",
          id: "68B6B341A81C-8",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LTP-3 F35 DB-05-MPP_WM/PP",
          id: "68B6B341A81C-9",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 03 F36 DB-31-CHILLER YARD",
          id: "68B6B341A81C-10",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 03 F37 DB-01-MPP",
          id: "68B6B341A81C-11",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LTP-3 F38 DB-07-MPP_TW/LW/CW/VF",
          id: "68B6B341A81C-12",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 03 F39 SSPDB-174 & 175 LT ROOM",
          id: "68B6B341A81C-13",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 03 DG I/C-2",
          id: "68B6B341A81C-15",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
      ],
    },
    position: {
      x: 267.5084437774026,
      y: 891.8926574742311,
    },
    width: 471,
    height: 467,
    selected: false,
    dragging: false,
  },
  {
    id: "42",
    type: "custom",
    mete: "energy",
    data: {
      text: "PANEl 02",
      description: true,
      handlers: [
        {
          handle: {
            type: "target",
            handleId: "a",
            position: "top",
          },
        },
      ],
      style: {
        width: 450,
        height: "auto",
        borderRadius: 8,
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "10px",
        textAlign: "center",
      },
      energyMeters: [
        {
          text: "LT Panel 02 I/C from DG SET 02",
          status: "not",
          id: "68B6B341A86C-17",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 02 F15 DB-10-NEW HVT",
          id: "68B6B341A86C-18",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 02 F16 DB-13",
          id: "68B6B341A86C-19",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 02 F17 DB- - SPARE",
          id: "68B6B341A86C-20",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 02 F18 DB-42-NEW TP AREA",
          id: "68B6B341A86C-21",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 02 F19 DB-11-OLD HVT",
          id: "68B6B341A86C-22",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 02 F20 DB- - SPARE",
          id: "68B6B341A86C-23",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 02 F21 DB-08- RM STORE AREA",
          id: "68B6B341A86C-24",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 02 F22 DB-13- ENGG OFFICE",
          id: "68B6B341A86C-25",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 02 F23 DB-25- A-ROOM",
          id: "68B6B341A86C-26",
          status: "not",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 02 F25 DB-18- ENGG LAB",
          id: "68B6B341A86C-28",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 02 F26 DB-23 & 23A - GLASS SHOP",
          id: "68B6B341A86C-29",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 02 F28 DB-24- ENGG LAB",
          id: "68B6B341A86C-31",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
        {
          text: "LT Panel 02 F24 DB-16- MPP PROCESS AREA",
          id: "68B6B341A86C-27",
          imageUrl:
            "https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg",
        },
      ],
    },
    position: {
      x: -227.5084437774026,
      y: 891.8926574742311,
    },
    width: 471,
    height: 599,
    selected: false,
    dragging: false,
  },
];

// Existing edges...
const initialEdges = [
  {
    id: "e4",
    source: "1",
    sourceHandle: "a",
    target: "5",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e5",
    source: "5",
    sourceHandle: "c",
    target: "6",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e6",
    source: "5",
    sourceHandle: "b",
    target: "7",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e7",
    source: "5",
    sourceHandle: "d",
    target: "8",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e8",
    source: "5",
    sourceHandle: "d",
    target: "9",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e13",
    source: "6",
    sourceHandle: "b",
    target: "14",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e14",
    source: "14",
    sourceHandle: "b",
    target: "10",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e15",
    source: "7",
    sourceHandle: "b",
    target: "15",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e16",
    source: "15",
    sourceHandle: "b",
    target: "11",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e17",
    source: "8",
    sourceHandle: "b",
    target: "16",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e18",
    source: "16",
    sourceHandle: "b",
    target: "12",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e19",
    source: "9",
    sourceHandle: "b",
    target: "17",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e20",
    source: "17",
    sourceHandle: "b",
    target: "13",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e21",
    source: "10",
    sourceHandle: "b",
    target: "18",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e22",
    source: "11",
    sourceHandle: "b",
    target: "19",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e23",
    source: "20",
    sourceHandle: "a",
    target: "20",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e24",
    source: "3",
    sourceHandle: "b",
    target: "20",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e25",
    source: "19",
    sourceHandle: "b",
    target: "21",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e26",
    source: "18",
    sourceHandle: "b",
    target: "21",
    targetHandle: "b",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e29",
    source: "13",
    sourceHandle: "b",
    target: "22",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e30",
    source: "23",
    sourceHandle: "a",
    target: "22",
    targetHandle: "c",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e31",
    source: "20",
    sourceHandle: "a",
    target: "21",
    targetHandle: "c",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e32",
    source: "21",
    sourceHandle: "d",
    target: "24",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e33",
    source: "21",
    sourceHandle: "d",
    target: "26",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e34",
    source: "21",
    sourceHandle: "d",
    target: "28",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e35",
    source: "30",
    sourceHandle: "a",
    target: "21",
    targetHandle: "c",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e36",
    source: "31",
    sourceHandle: "a",
    target: "21",
    targetHandle: "c",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e37",
    source: "32",
    sourceHandle: "a",
    target: "21",
    targetHandle: "c",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e38",
    source: "12",
    sourceHandle: "b",
    target: "34",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e39",
    source: "12",
    sourceHandle: "b",
    target: "35",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e40",
    source: "22",
    sourceHandle: "b",
    target: "36",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e41",
    source: "36",
    sourceHandle: "b",
    target: "37",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e42",
    source: "34",
    sourceHandle: "b",
    target: "38",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e43",
    source: "35",
    sourceHandle: "b",
    target: "38",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e44",
    source: "30",
    sourceHandle: "b",
    target: "39",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e45",
    source: "32",
    sourceHandle: "b",
    target: "39",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e46",
    source: "33",
    sourceHandle: "a",
    target: "39",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e47",
    source: "31",
    sourceHandle: "b",
    target: "39",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e48",
    source: "28",
    sourceHandle: "b",
    target: "40",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e49",
    source: "29",
    sourceHandle: "a",
    target: "40",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e50",
    source: "26",
    sourceHandle: "b",
    target: "41",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e51",
    source: "27",
    sourceHandle: "a",
    target: "41",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e52",
    source: "24",
    sourceHandle: "b",
    target: "42",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
  {
    id: "e53",
    source: "25",
    sourceHandle: "a",
    target: "42",
    targetHandle: "a",
    type: "smoothstep",
    animated: true,
  },
];
function Flow() {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [nextNodeId, setNextNodeId] = useState(3); // Start from 3 since initial nodes are 1 and 2
  const [nextEdgeId, setNextEdgeId] = useState(2); // Start from 2 since initial edge is e1-2
  const [currentComponent, setCurrentComponent] = useState(null);
  const { themes } = useTheme();
  const [currentNodeData, setCurrentNodeData] = useState(null); // New state for node data

  useEffect(() => {
    const savedNodes = localStorage.getItem("reactFlowNodes");
    const savedEdges = localStorage.getItem("reactFlowEdges");
    const savedNextNodeId = localStorage.getItem("reactFlowNextNodeId");
    const savedNextEdgeId = localStorage.getItem("reactFlowNextEdgeId");

    if (savedNodes) {
      const parsedNodes = JSON.parse(savedNodes);
      setNodes(parsedNodes);
      const maxNodeId = parsedNodes.reduce(
        (max, node) => Math.max(max, parseInt(node.id)),
        0
      );
      setNextNodeId(maxNodeId + 1);
    } else {
      setNodes(initialNodes);
      setNextNodeId(initialNodes.length + 1);
    }

    if (savedEdges) {
      const parsedEdges = JSON.parse(savedEdges);
      setEdges(parsedEdges);
      const maxEdgeId = parsedEdges.reduce(
        (max, edge) => Math.max(max, parseInt(edge.id.replace("e", "")), 0),
        0
      );
      setNextEdgeId(maxEdgeId + 1);
    } else {
      setEdges(initialEdges);
      setNextEdgeId(initialEdges.length + 1);
    }

    if (savedNextNodeId) {
      setNextNodeId(parseInt(savedNextNodeId));
    }

    if (savedNextEdgeId) {
      setNextEdgeId(parseInt(savedNextEdgeId));
    }
  }, []);

  // Handle node and edge changes
  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );

  const onEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );

  const onConnect = useCallback(
    (connection) => {
      const { sourceHandle, targetHandle } = connection;

      if (!sourceHandle || !targetHandle) {
        alert("Please connect using valid handles.");
        return;
      }

      const newEdge = {
        id: `e${nextEdgeId}`,
        source: connection.source,
        sourceHandle,
        target: connection.target,
        targetHandle,
        type: "smoothstep",
        animated: true,
      };

      setEdges((eds) => addEdge(newEdge, eds));
      setNextEdgeId(nextEdgeId + 1);
    },
    [nextEdgeId]
  );

  // Handle adding a new node

  // Handle node click for editing

  const handleNodeClick = (_, node) => {
    if (node.id === "1") {
      setCurrentComponent("Sustainability");
      setCurrentNodeData(node.data); // Save node data
    } else if (node.mete === "energy") {
      setCurrentComponent("Energy");
      setCurrentNodeData(node.data); // Save node data
    } else if (node.id === "3") {
      setCurrentComponent("Process2");
    } else if (node.id === "4") {
      setCurrentComponent("EndComponent");
    }
  };

  const renderCurrentComponent = () => {
    if (currentComponent === "Energy") {
      // You can dynamically set the font size as needed
      const fontSize = "0.9rem"; // Example: You can set this to a variable or calculate it dynamically

      return (
        <div style={{ width: "100%", height: "100%", position: "relative" }}>
          <Energy
            headerText={
              currentNodeData?.energyMeters?.[0]?.text || // Use the first text in the array
              currentNodeData?.text ||
              "Energy Component"
            }
            fontSize={fontSize} // Pass the font size prop to Energy component
            showBackButton={true} // Show back button
            onBackButtonClick={() => {
              setCurrentComponent(null);
              setCurrentNodeData(null); // Reset node data
            }}
          />
        </div>
      );
    } else if (currentComponent === "Sustainability") {
      return (
        <div style={{ width: "100%", height: "100%", position: "relative" }}>
          <Sustainability
            showBackButton={true} // Pass showBackButton flag to show the back button
            onBackButtonClick={() => {
              setCurrentComponent(null);
              setCurrentNodeData(null); // Reset node data
            }}
          />
        </div>
      );
    }
    return null;
  };
  return (
    <div className="flow-container">
      {!currentComponent && (
        <CardHeader headerText="Power Distribution Viewer" />
      )}
      <div style={{ display: "flex", height: "92vh" }}>
        {currentComponent ? (
          renderCurrentComponent()
        ) : (
          <ReactFlowProvider>
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              nodeTypes={nodeTypes}
              fitView
              onNodeClick={handleNodeClick}
              style={{
                backgroundColor: themes === "dark" ? "black" : "#FFFEFE",
              }}
            >
              <Background />
              <Controls />
            </ReactFlow>

            <div
              style={{
                position: "absolute",
                top: "145px",
                right: "10px",
                backgroundColor: themes === "dark" ? "#2E2E2E" : "#FFFFFF",
                padding: "10px",
                border: `1px solid ${themes === "dark" ? "black" : "#CCCCCC"}`,
                borderRadius: "4px",
                zIndex: 10, // Ensure it appears above ReactFlow
                color: themes === "dark" ? "#FFFFFF" : "#000000",
                fontSize: "14px",
              }}
            >
              <ul style={{ listStyleType: "none", padding: 0, margin: 0 }}>
                <li
                  style={{
                    marginBottom: "8px",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  <img
                    src="https://res.cloudinary.com/dp6envw5o/image/upload/v1678345927/Group_29506_cdgdk8.svg"
                    alt="Node Type A"
                    style={{
                      width: "20px",
                      height: "20px",
                      marginRight: "8px",
                    }}
                  />
                  Building
                </li>
                <li
                  style={{
                    marginBottom: "8px",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  <img
                    src="https://res.cloudinary.com/dujhloknt/image/upload/v1733395030/transformer_mlhadr.png"
                    alt="Node Type B"
                    style={{
                      width: "20px",
                      height: "20px",
                      marginRight: "8px",
                    }}
                  />
                  Transformer
                </li>
                <li
                  style={{
                    marginBottom: "8px",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  <img
                    src="https://res.cloudinary.com/dqexqku43/image/upload/v1677184686/Group_29544_tctvfu.jpg"
                    alt="Node Type C"
                    style={{
                      width: "20px",
                      height: "20px",
                      marginRight: "8px",
                    }}
                  />
                  Energy Meter
                </li>
                <li
                  style={{
                    marginBottom: "8px",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  <img
                    src="https://res.cloudinary.com/dujhloknt/image/upload/v1733829925/Panel_dzvgsn.png"
                    alt="Node Type C"
                    style={{
                      width: "20px",
                      height: "20px",
                      marginRight: "8px",
                    }}
                  />
                  LT Panel
                </li>
                <li
                  style={{
                    marginBottom: "8px",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  <img
                    src="https://res.cloudinary.com/dujhloknt/image/upload/v1733829960/DRUPS_kcmvwu.png"
                    alt="Node Type C"
                    style={{
                      width: "20px",
                      height: "20px",
                      marginRight: "8px",
                    }}
                  />
                  DRUPS
                </li>

                <li
                  style={{
                    marginBottom: "8px",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  <img
                    src="https://res.cloudinary.com/dujhloknt/image/upload/v1733829925/BusBar_judesm.png"
                    alt="Node Type C"
                    style={{
                      width: "20px",
                      height: "20px",
                      marginRight: "8px",
                    }}
                  />
                  Busbar
                </li>
                <li
                  style={{
                    marginBottom: "8px",
                    display: "flex",
                    alignItems: "center",
                  }}
                >
                  <img
                    src="              https://res.cloudinary.com/dujhloknt/image/upload/v1733839407/DG_hhnkq5.png
"
                    alt="Node Type C"
                    style={{
                      width: "20px",
                      height: "20px",
                      marginRight: "8px",
                    }}
                  />
                  DG-SET
                </li>
              </ul>
            </div>

            {nodes.map((node) => {
              if (node.type === "group") {
                const childNodes = nodes.filter(
                  (n) => n.data.parent === node.id
                );
                return (
                  <div
                    key={node.id}
                    style={{
                      position: "absolute",
                      top: node.position.y,
                      left: node.position.x,
                    }}
                  >
                    {/* Render the group node */}
                    <div
                      style={{
                        padding: "10px",
                        border: "1px solid black",
                        borderRadius: "4px",
                      }}
                    >
                      {node.data.text}
                    </div>
                    {childNodes.map((child) => (
                      <div
                        key={child.id}
                        style={{
                          position: "absolute",
                          top: 20,
                          left: 20,
                        }}
                      >
                        {/* Render child node */}
                        <div
                          style={{
                            padding: "5px",
                            border: "1px solid gray",
                            borderRadius: "4px",
                          }}
                        >
                          {child.data.text}
                        </div>
                      </div>
                    ))}
                  </div>
                );
              }
              return null;
            })}
          </ReactFlowProvider>
        )}
      </div>
    </div>
  );
}

export default Flow;
