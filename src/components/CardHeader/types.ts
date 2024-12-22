export type ChildrenProps = {
  children: string | JSX.Element | JSX.Element[];
  headerText: string;
  filter?: boolean;
  subHeader?: string;
  expand?: boolean;
  setDialog?: React.Dispatch<React.SetStateAction<boolean>>;
  filterText?: string;
  handleFilter?: (filter: string) => void;
  activeGroupFilter?: string;
};
