const nodeExcel = require("excel-export");

const getPerson = (db, req, res, next) => {
    db.sequelize.query("select name, person from interest_person_top10", {
        type: db.sequelize.QueryTypes.SELECT
    }).then((selectPersonRes) => {
        const xData = [];
        const yData = [];
        selectPersonRes.map((item) => {
            xData.push(item.name);
            yData.push(item.person);
        });
        res.json([xData, yData]);
    });
};

const getWeight = (db, req, res, next) => {
    db.sequelize.query("select w as value, name from interest_w_top10", {
        type: db.sequelize.QueryTypes.SELECT
    }).then((selectWRes) => {
        const legend = [];
        selectWRes.map((item) => {
            legend.push(item.name);
        });
        res.json([legend, selectWRes]);
    });
};

const getHindex = (db, req, res, next) => {
    if (req.query.search == null || req.query.search == "") {
        db.sequelize.query("select user_h_index.user_id, name, paper, citation, user.h_index, g_index, sociability, diversity, activity from user join user_h_index on user.user_id = user_h_index.user_id limit ?, ?", {
            replacements: [parseInt(req.query.offset), parseInt(req.query.limit)],
            type: db.sequelize.QueryTypes.SELECT
        }).then((selectUH) => {
            db.sequelize.query("select count(user_id) as nums from user", {
                type: db.sequelize.QueryTypes.SELECT
            }).then((selectUserRes) => {
                res.json({
                    total: selectUserRes[0].nums,
                    rows: selectUH
                });
            });
        });
    }
    else {
        const search = req.query.search;
        const offset = req.query.offset;
        const limit = req.query.limit;
        let rowSql = `select user_h_index.user_id, name, paper, citation, user.h_index, g_index, sociability, diversity, activity from user join user_h_index on user.user_id = user_h_index.user_id where name like '%${search}%' or paper like '%${search}%' or citation like '%${search}%' or user.h_index like '%${search}%' or g_index like '%${search}%' or sociability like '%${search}%' or diversity like '%${search}%' or activity like '%${search}%' limit ${offset}, ${limit};`;

        let totalSql = `select user_h_index.user_id, name, paper, citation, user.h_index, g_index, sociability, diversity, activity from user join user_h_index on user.user_id = user_h_index.user_id where name like '%${search}%' or paper like '%${search}%' or citation like '%${search}%' or user.h_index like '%${search}%' or g_index like '%${search}%' or sociability like '%${search}%' or diversity like '%${search}%' or activity like '%${search}%';`;
        console.log(rowSql);
        db.sequelize.query(rowSql, {
            type: db.sequelize.QueryTypes.SELECT
        }).then((selectUH) => {
            db.sequelize.query(totalSql, {
                type: db.sequelize.QueryTypes.SELECT
            }).then((selectTotalUserRes) => {
                res.json({
                    total: selectTotalUserRes.length,
                    rows: selectUH
                });
            });
        });
    }
    
};

const formatResult = (selectRes) => {
    const result = [];
    selectRes.map((item) => {
        const row = [];
        row.push(item.name);
        row.push(item.h_index);
        row.push(item.paper);
        row.push(item.citation);
        row.push(item.g_index);
        row.push(item.sociability);
        row.push(item.diversity);
        row.push(item.activity);
        result.push(row);
    });
    return result;
};

const exportExcel = (db, req, res, next) => {
    db.sequelize.query("select user_h_index.user_id, name, paper, citation, user.h_index, g_index, sociability, diversity, activity from user join user_h_index on user.user_id = user_h_index.user_id", {
        type: db.sequelize.QueryTypes.SELECT
    }).then((result) => {
        var conf = {};
        conf.name = "aminers";
        conf.cols = [
            {
                caption: "name",
                type: "string",
                width: 30
            }, 
            {
                caption:"h_index",
                type:"number"				
            }, 
            {
                caption:"paper",
                type:"number"				
            }, 
            {
                caption:"citation",
                type:"number"				
            },
            {
                caption:"g_index",
                type:"number"				
            },
            {
                caption:"sociability",
                type:"number"				
            },
            {
                caption:"diversity",
                type:"number"				
            },
            {
                caption:"activity",
                type:"number"				
            }
        ];
        conf.rows = formatResult(result);
        var excelFile = nodeExcel.execute(conf);
        res.setHeader('Content-Type', 'application/vnd.openxmlformats');
        res.setHeader("Content-Disposition", "attachment; filename=" + "export_aminer.xlsx");
        res.end(excelFile, "binary");
    });
};

const commonController = {};
commonController.getPerson = getPerson;
commonController.getWeight = getWeight;
commonController.getHindex = getHindex;
commonController.exportExcel = exportExcel;

module.exports = commonController;