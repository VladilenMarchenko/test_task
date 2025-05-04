import {Route, Routes} from "react-router-dom";
import UploadingPage from "./Uploading/UploadingPage";
import {RouterNames} from "./RouterNames";
import ImagesPage from "./Images/ImagesPage";
import StatisticsPage from "./Statistics/StatisticsPage";


const AppRouter = () => {
    return (
        <Routes>
            <Route path={RouterNames.UploadingPage.path} element={<UploadingPage/>}/>
            <Route path={RouterNames.ImagesPage.path} element={<ImagesPage/>}/>
            <Route path={RouterNames.StatisticPage.path} element={<StatisticsPage/>}/>
        </Routes>
    );
};

export default AppRouter;