import React, { useCallback, useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { FileText, Download, Mail } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { api } from '@/lib/api';
import type { Report, ReportPreferences } from '@/types/api';

export const ReportManagement: React.FC = () => {
  const [preferences, setPreferences] = useState<ReportPreferences>({
    delivery_time: "09:00",
    email_enabled: true,
    pdf_enabled: true,
    delivery_method: ['email', 'in_app'],
    schedule_time: '09:00',
    timezone: 'Asia/Shanghai'
  });
  const [reports, setReports] = useState<Report[]>([]);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();

  const fetchData = useCallback(async () => {
    try {
      const [prefsRes, reportsRes] = await Promise.all([
        api.fetchReportPreferences(),
        api.fetchReports()
      ]);
      setPreferences(prefsRes.data.data);
      setReports(reportsRes.data.data);
    } catch (error) {
      void error;
      toast({
        variant: "destructive",
        title: "错误",
        description: "加载报告设置失败",
      });
    } finally {
      setLoading(false);
    }
  }, [toast]);

  const handleGenerateReport = async () => {
    try {
      await api.generateReport();
      toast({
        title: "生成中",
        description: "报告正在生成，请稍后查看",
      });
    } catch (error) {
      void error;
      toast({
        variant: "destructive",
        title: "错误",
        description: "生成报告失败",
      });
    }
  };

  const handleSavePreferences = async () => {
    try {
      await api.updateReportPreferences(preferences);
      toast({
        title: "成功",
        description: "报告设置已保存",
      });
    } catch (error) {
      void error;
      toast({
        variant: "destructive",
        title: "错误",
        description: "保存设置失败",
      });
    }
  };

  const handleDownload = async (reportId: number) => {
    try {
      const response = await api.downloadReport(reportId);
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report-${reportId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      void error;
      toast({
        variant: "destructive",
        title: "错误",
        description: "下载报告失败",
      });
    }
  };

  const handleEmailReport = async (reportId: number) => {
    try {
      await api.emailReport(reportId);
      toast({
        title: "成功",
        description: "报告已发送至您的邮箱",
      });
    } catch (error) {
      void error;
      toast({
        variant: "destructive",
        title: "错误",
        description: "发送报告失败",
      });
    }
  };

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  if (loading) {
    return <div className="flex justify-center items-center h-64">加载中...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">报告管理</h1>
        <Button onClick={handleGenerateReport}>
          <FileText className="w-4 h-4 mr-2" />
          立即生成
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>报告设置</CardTitle>
          <CardDescription>配置您的报告生成和发送偏好</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <Label htmlFor="delivery-time">每日发送时间</Label>
              <Select
                value={preferences.delivery_time}
                onValueChange={(value) => setPreferences({ ...preferences, delivery_time: value })}
              >
                <SelectTrigger className="w-40">
                  <SelectValue placeholder="选择时间" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="09:00">09:00</SelectItem>
                  <SelectItem value="12:00">12:00</SelectItem>
                  <SelectItem value="15:00">15:00</SelectItem>
                  <SelectItem value="18:00">18:00</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>邮件发送</Label>
                <p className="text-sm text-muted-foreground">通过邮件接收报告</p>
              </div>
              <Switch
                checked={preferences.email_enabled}
                onCheckedChange={(checked) => setPreferences({ ...preferences, email_enabled: checked })}
                aria-label="邮件发送"
              />
            </div>

            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label>PDF导出</Label>
                <p className="text-sm text-muted-foreground">启用PDF导出选项</p>
              </div>
              <Switch
                checked={preferences.pdf_enabled}
                onCheckedChange={(checked) => setPreferences({ ...preferences, pdf_enabled: checked })}
                aria-label="PDF导出"
              />
            </div>
          </div>

          <Button onClick={handleSavePreferences} className="w-full">
            保存设置
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>最近报告</CardTitle>
          <CardDescription>查看和下载最近生成的报告</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {reports.map((report) => (
              <div key={report.id} className="flex items-center justify-between p-4 border rounded-lg">
                <div>
                  <p className="font-medium">{report.type}</p>
                  <p className="text-sm text-muted-foreground">{report.date}</p>
                </div>
                <div className="space-x-2">
                  {preferences.email_enabled && (
                    <Button
                      size="icon"
                      variant="outline"
                      onClick={() => handleEmailReport(report.id)}
                    >
                      <Mail className="w-4 h-4" />
                    </Button>
                  )}
                  {preferences.pdf_enabled && (
                    <Button
                      size="icon"
                      variant="outline"
                      onClick={() => handleDownload(report.id)}
                    >
                      <Download className="w-4 h-4" />
                    </Button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
