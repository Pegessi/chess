<template>
  <div>
    <!--面包屑导航区域-->
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>好友管理</el-breadcrumb-item>
      <el-breadcrumb-item>好友请求</el-breadcrumb-item>
    </el-breadcrumb>
    <el-row :gutter="12">
      <el-col :span="12">
        <!--收到的请求-->
        <el-card>
          <div slot="header" class="clearfix">
            <span>收到的请求</span>
            <el-button style="float: right; padding: 3px 0" type="text">清空已处理请求</el-button>
          </div>
          <el-table
            :data="recList"
            style="width: 100%">
            <el-table-column
              label="日期"
              width="180">
              <template slot-scope="scope">
                <i class="el-icon-time"></i>
                <span style="margin-left: 10px">{{ scope.row.pk }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="来自"
              width="180">
              <template slot-scope="scope">
                <span>{{ scope.row.fields.send }}</span>
              </template>
            </el-table-column>
            <el-table-column label="状态">
              <template slot-scope="scope">
                <span>{{scope.row.fields.flag}}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  type="success"
                  style="padding: 7px"
                  plain
                  @click="handleEdit(scope.$index, scope.row)"
                  :disabled="(scope.row.fields.flag==='未处理')?false:true">接受
                </el-button>
                <el-button
                  size="mini"
                  style="padding: 7px"
                  @click="handleRefuse(scope.$index, scope.row)"
                  :disabled="(scope.row.fields.flag==='未处理')?false:true">拒绝
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <div slot="header" class="clearfix">
            <span>发送的请求</span>
            <el-button style="float: right; padding: 3px 0" type="text">清空已处理请求</el-button>
          </div>
          <el-table
            :data="sendList"
            style="width: 100%">
            <el-table-column
              label="日期"
              width="180">
              <template slot-scope="scope">
                <i class="el-icon-time"></i>
                <span style="margin-left: 10px">{{ scope.row.pk }}</span>
              </template>
            </el-table-column>
            <el-table-column
              label="发向"
              width="180">
              <template slot-scope="scope">
                <span>{{ scope.row.fields.receive }}</span>
              </template>
            </el-table-column>
            <el-table-column label="状态">
              <template slot-scope="scope">
                <span>{{scope.row.fields.flag}}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  type="danger"
                  plain
                  @click="handleDelete(scope.$index, scope.row)"
                  :disabled="(scope.row.fields.flag==='未处理')?false:true">撤销
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  export default {
    name: "reqfri",
    mounted() {
      this.getSendList()
      this.getRecList()
    },
    data() {
      return {
        sendList: [],
        recList: []
      }
    },
    methods: {
      getSendList() {
        this.$http.get('selectSendReq?send=' + window.sessionStorage.getItem('id')).then(res => {
          this.sendList = res.data.reqList
          for (var i in this.sendList) {
            this.sendList[i].pk = this.sendList[i].pk.toString().split(' ')[0]
          }
          // console.log(this.sendList)
        })
      },
      getRecList() {
        this.$http.get('selectRecReq?rec=' + window.sessionStorage.getItem('id')).then(res => {
          this.recList = res.data.reqList
          for (var i in this.recList) {
            this.recList[i].pk = this.recList[i].pk.toString().split(' ')[0]
          }
          // console.log(this.sendList)
        })
      },
      handleEdit(index, row) {
        // 同意请求
        var send = row.fields.send
        var rec = row.fields.receive
        var flag = '同意'
        console.log(send)
        this.$http.get('dealReq?send=' + send + '&rec=' + rec + '&flag=' + flag).then(res => {
          this.getRecList()
          this.$message.success('请求处理成功！')
        })
        // console.log(index, row);
      },
      handleRefuse(index, row) {
        var send = row.fields.send
        var rec = row.fields.receive
        var flag = '拒绝'
        this.$http.get('dealReq?send=' + send + '&rec=' + rec + '&flag=' + flag).then(res => {
          this.getRecList()
          this.$message.success('请求处理成功！')
        })
      },
      handleDelete(index, row) {
        // 删除请求
        var send = row.fields.send
        var rec = row.fields.receive
        this.$http.get('delReq?send=' + send + '&rec=' + rec).then(res => {
          this.getSendList()
          this.$message.success('撤销成功！')
        })
      }
    }
  }
</script>

<style scoped>

</style>
