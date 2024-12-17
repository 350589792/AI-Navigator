import React, { useCallback } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { X } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { api } from '@/lib/api';
import type { Category, UserPreferences, ApiResponse } from '@/types/api';

export const PreferenceSettings: React.FC = () => {
  const [categories, setCategories] = React.useState<Category[]>([]);
  const [selectedCategories, setSelectedCategories] = React.useState<number[]>([]);
  const [keywords, setKeywords] = React.useState<string[]>([]);
  const [newKeyword, setNewKeyword] = React.useState('');
  const [scheduleTime, setScheduleTime] = React.useState('09:00');
  const [timezone, setTimezone] = React.useState(Intl.DateTimeFormat().resolvedOptions().timeZone);
  const [loading, setLoading] = React.useState(true);
  const { toast } = useToast();

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      const [categoriesRes, preferencesRes] = await Promise.all([
        api.get<ApiResponse<Category[]>>('/api/v1/data-sources/categories'),
        api.get<ApiResponse<UserPreferences>>('/api/v1/preferences')
      ]);

      setCategories(categoriesRes.data.data);

      const prefs = preferencesRes.data.data;
      if (prefs) {
        setSelectedCategories(prefs.categories.map((cat: { id: number }) => cat.id));
        setKeywords(prefs.keywords || []);
        setScheduleTime(prefs.schedule_time || '09:00');
        setTimezone(prefs.timezone || Intl.DateTimeFormat().resolvedOptions().timeZone);
      }
    } catch (error) {
      void error; // Explicitly mark error as intentionally unused
      toast({
        variant: "destructive",
        title: "错误",
        description: "加载偏好设置失败",
      });
    } finally {
      setLoading(false);
    }
  }, [toast]);

  React.useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleAddKeyword = () => {
    if (newKeyword && !keywords.includes(newKeyword)) {
      setKeywords([...keywords, newKeyword]);
      setNewKeyword('');
    }
  };

  const handleRemoveKeyword = (keyword: string) => {
    setKeywords(keywords.filter((k) => k !== keyword));
  };

  const handleToggleCategory = (categoryId: number) => {
    setSelectedCategories((prev) =>
      prev.includes(categoryId)
        ? prev.filter((id) => id !== categoryId)
        : [...prev, categoryId]
    );
  };

  const handleSavePreferences = async () => {
    try {
      await api.post<ApiResponse<void>>('/api/v1/preferences', {
        categories: selectedCategories.map(id => ({ id })),
        keywords,
        schedule_time: scheduleTime,
        timezone
      });
      toast({
        title: "成功",
        description: "偏好设置已保存",
      });
    } catch (error) {
      void error; // Explicitly mark error as intentionally unused
      toast({
        variant: "destructive",
        title: "错误",
        description: "保存偏好设置失败",
      });
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">加载中...</div>;
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">订阅偏好设置</h2>

      <div className="space-y-2">
        <Label>分类</Label>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {categories.map((category) => (
            <Card
              key={category.id}
              className={`cursor-pointer ${
                selectedCategories.includes(category.id) ? 'border-primary' : ''
              }`}
              onClick={() => handleToggleCategory(category.id)}
            >
              <CardContent className="p-4">
                <h3 className="font-semibold">{category.name}</h3>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      <div className="space-y-2">
        <Label>关键词</Label>
        <div className="flex gap-2">
          <Input
            value={newKeyword}
            onChange={(e) => setNewKeyword(e.target.value)}
            placeholder="输入关键词"
            onKeyPress={(e) => e.key === 'Enter' && handleAddKeyword()}
          />
          <Button onClick={handleAddKeyword}>添加</Button>
        </div>
        <div className="flex flex-wrap gap-2 mt-2">
          {keywords.map((keyword) => (
            <Badge key={keyword} variant="secondary">
              {keyword}
              <X
                className="w-3 h-3 ml-1 cursor-pointer"
                onClick={() => handleRemoveKeyword(keyword)}
              />
            </Badge>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="scheduleTime">报告时间</Label>
          <Input
            id="scheduleTime"
            type="time"
            value={scheduleTime}
            onChange={(e) => setScheduleTime(e.target.value)}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="timezone">时区</Label>
          <select
            id="timezone"
            className="w-full p-2 border rounded"
            value={timezone}
            onChange={(e) => setTimezone(e.target.value)}
          >
            <option value="Asia/Shanghai">中国标准时间 (UTC+8)</option>
            <option value="Asia/Tokyo">日本标准时间 (UTC+9)</option>
            <option value="Asia/Singapore">新加坡标准时间 (UTC+8)</option>
            <option value="Asia/Seoul">韩国标准时间 (UTC+9)</option>
          </select>
        </div>
      </div>

      <Button onClick={handleSavePreferences} className="w-full">
        保存设置
      </Button>
    </div>
  );
};
