import { useState, useEffect } from 'react'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Database, FileText, Plus, RefreshCcw } from 'lucide-react'
import { API_BASE_URL } from './config'

interface DataSource {
  id: string
  name: string
  url: string
  status: string
}

interface Report {
  id: string
  title: string
  date: string
  status: string
}

function App() {
  const [dataSources, setDataSources] = useState<DataSource[]>([])
  const [reports, setReports] = useState<Report[]>([])
  const [newSourceUrl, setNewSourceUrl] = useState('')
  const [loading, setLoading] = useState({
    sources: false,
    reports: false,
    addSource: false,
    generateReport: false
  })

  useEffect(() => {
    fetchDataSources()
    fetchReports()
  }, [])

  const fetchDataSources = async () => {
    setLoading(prev => ({ ...prev, sources: true }))
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/data-sources`)
      const data = await response.json()
      setDataSources(data)
    } catch (error) {
      console.error('Error fetching data sources:', error)
    } finally {
      setLoading(prev => ({ ...prev, sources: false }))
    }
  }

  const fetchReports = async () => {
    setLoading(prev => ({ ...prev, reports: true }))
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/reports`)
      const data = await response.json()
      setReports(data)
    } catch (error) {
      console.error('Error fetching reports:', error)
    } finally {
      setLoading(prev => ({ ...prev, reports: false }))
    }
  }

  const addDataSource = async () => {
    if (!newSourceUrl) return
    setLoading(prev => ({ ...prev, addSource: true }))
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/data-sources`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: newSourceUrl })
      })
      if (response.ok) {
        setNewSourceUrl('')
        fetchDataSources()
      }
    } catch (error) {
      console.error('Error adding data source:', error)
    } finally {
      setLoading(prev => ({ ...prev, addSource: false }))
    }
  }

  const generateReport = async () => {
    setLoading(prev => ({ ...prev, generateReport: true }))
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/reports`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: `Daily Report ${new Date().toLocaleDateString()}` })
      })
      if (response.ok) {
        fetchReports()
      }
    } catch (error) {
      console.error('Error generating report:', error)
    } finally {
      setLoading(prev => ({ ...prev, generateReport: false }))
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="mx-auto max-w-7xl">
        <h1 className="mb-8 text-3xl font-bold text-gray-900">AI Navigator</h1>

        <Tabs defaultValue="sources" className="space-y-4">
          <TabsList>
            <TabsTrigger value="sources">
              <Database className="mr-2 h-4 w-4" />
              数据源管理
            </TabsTrigger>
            <TabsTrigger value="reports">
              <FileText className="mr-2 h-4 w-4" />
              报告生成
            </TabsTrigger>
          </TabsList>

          <TabsContent value="sources">
            <Card>
              <CardHeader>
                <CardTitle>数据源管理</CardTitle>
                <CardDescription>添加和管理您的数据源</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex space-x-2 mb-4">
                  <Input
                    placeholder="输入数据源URL"
                    value={newSourceUrl}
                    onChange={(e) => setNewSourceUrl(e.target.value)}
                  />
                  <Button
                    onClick={addDataSource}
                    disabled={loading.addSource || !newSourceUrl}
                  >
                    <Plus className="mr-2 h-4 w-4" />
                    {loading.addSource ? '添加中...' : '添加数据源'}
                  </Button>
                </div>

                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>名称</TableHead>
                      <TableHead>URL</TableHead>
                      <TableHead>状态</TableHead>
                      <TableHead>操作</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {loading.sources ? (
                      <TableRow>
                        <TableCell colSpan={4} className="text-center">加载中...</TableCell>
                      </TableRow>
                    ) : dataSources.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={4} className="text-center">暂无数据源</TableCell>
                      </TableRow>
                    ) : (
                      dataSources.map((source) => (
                        <TableRow key={source.id}>
                          <TableCell>{source.name}</TableCell>
                          <TableCell>{source.url}</TableCell>
                          <TableCell>{source.status}</TableCell>
                          <TableCell>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => fetchDataSources()}
                            >
                              <RefreshCcw className="mr-2 h-4 w-4" />
                              更新
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="reports">
            <Card>
              <CardHeader>
                <CardTitle>报告管理</CardTitle>
                <CardDescription>生成和查看智能报告</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="mb-4">
                  <Button
                    onClick={generateReport}
                    disabled={loading.generateReport}
                  >
                    <Plus className="mr-2 h-4 w-4" />
                    {loading.generateReport ? '生成中...' : '生成新报告'}
                  </Button>
                </div>

                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>标题</TableHead>
                      <TableHead>日期</TableHead>
                      <TableHead>状态</TableHead>
                      <TableHead>操作</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {loading.reports ? (
                      <TableRow>
                        <TableCell colSpan={4} className="text-center">加载中...</TableCell>
                      </TableRow>
                    ) : reports.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={4} className="text-center">暂无报告</TableCell>
                      </TableRow>
                    ) : (
                      reports.map((report) => (
                        <TableRow key={report.id}>
                          <TableCell>{report.title}</TableCell>
                          <TableCell>{report.date}</TableCell>
                          <TableCell>{report.status}</TableCell>
                          <TableCell>
                            <Button variant="outline" size="sm">
                              <FileText className="mr-2 h-4 w-4" />
                              查看
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))
                    )}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App
