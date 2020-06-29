<template>
  <div>
    <!--面包屑导航区域-->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>个人中心</el-breadcrumb-item>
      <el-breadcrumb-item>历史对局</el-breadcrumb-item>
    </el-breadcrumb>
    <!--卡片区域-->
    <el-card class="box-card">
      <!--搜索框区域-->
      <el-row :gutter="20">
        <el-col :span="14">
          <!-- style="margin-top: 15px;"-->
          <div>
            <el-input placeholder="请输入对手名称/日期" v-model="searchInput" class="input-with-select">
              <el-select v-model="select" slot="prepend" placeholder="请选择">
                <el-option label="最近七天" value="1"></el-option>
                <el-option label="所有" value="2"></el-option>
                <el-option label="胜局" value="3"></el-option>
                <el-option label="负局" value="4"></el-option>
              </el-select>
              <el-button slot="append" icon="el-icon-search"></el-button>
            </el-input>
          </div>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" plain>重置</el-button>
        </el-col>
      </el-row>
      <!--表格区域-->
      <el-table
        :data="this.passList"
        border
        stripe
        max-height="400">

        <el-table-column type="index"></el-table-column>
        <el-table-column label="时间" prop="pk"></el-table-column>
        <el-table-column label="对手" prop="fields.red"></el-table-column>
        <el-table-column label="战果" prop="fields.win">
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button
              size="mini"
              @click="handleEdit(scope.$index, scope.row)">查看对局
            </el-button>
            <!--<el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)">删除
            </el-button>-->
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>


</template>

<script>
  export default {
    name: "histroy",
    mounted() {
      this.username = window.sessionStorage.getItem('id')
      this.getPassList()
    },
    data() {
      return {
        username: '',
        searchInput: '',
        select: '',
        passList: [],
      }
    },
    methods: {
      handleEdit(index, row) {
        console.log(index, row);
      },
      handleDelete(index, row) {
        console.log(index, row);
      },
      tableRowClassName({row, rowIndex}) {
        if (rowIndex === 1) {
          return 'warning-row';
        } else if (rowIndex === 3) {
          return 'success-row';
        }
        return '';
      },
      getPassList() {
        this.$http.get('getPass?id=' + this.username).then(res => {
          // console.log(res)
          var passListR = res.data.redList
          var passListB = res.data.blackList
          var index = passListR
          for (var i in passListR) {
            passListR[i].pk = passListR[i].pk.toString().split(' ')[0]
            if(passListR[i].fields.win === this.username){
              passListR[i].fields.win = '胜'
            }else{
               passListR[i].fields.win = '负'
            }
          }
          for (var i in passListB) {
            passListB[i].pk = passListB[i].pk.toString().split(' ')[0]
            if(passListB[i].fields.win === this.username){
              passListB[i].fields.win = '胜'
            }else{
               passListB[i].fields.win = '负'
            }
            index.push(passListB[i])
          }
          this.passList = index
          console.log(this.passList)
        })
      }
    }
  }
</script>

<style scoped>
  .box-card {
    width: 100%;
    /*box-shadow: 0 1px 1px rgba(0, 0, 0, 0.15);*/
  }

  .el-select .el-input {
    width: 130px;
  }

  .input-with-select .el-input-group__prepend {
    background-color: #fff;
  }

  .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
</style>
