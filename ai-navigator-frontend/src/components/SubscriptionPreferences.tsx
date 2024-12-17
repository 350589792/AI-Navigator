import React, { useCallback } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";
import { api } from '@/lib/api';
import type { Category, UserPreferences, ApiResponse } from '@/types/api';
import { Badge } from "@/components/ui/badge";
import { X, Loader2 } from "lucide-react";

export const SubscriptionPreferences: React.FC = () => {
  const [categories, setCategories] = React.useState<Category[]>([]);
  const [selectedCategories, setSelectedCategories] = React.useState<number[]>([]);
  const [keywords, setKeywords] = React.useState<string[]>([]);
  const [newKeyword, setNewKeyword] = React.useState('');
  const [loading, setLoading] = React.useState(true);
  const [generating, setGenerating] = React.useState(false);
  const { toast } = useToast();

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      const [categoriesRes, preferencesRes] = await Promise.all([
        api.get<ApiResponse<Category[]>>('/api/v1/data-sources/categories'),
        api.get<ApiResponse<UserPreferences>>('/api/v1/preferences')
      ]);

      setCategories(categoriesRes.data.data);
      const preferences = preferencesRes.data.data;
      setSelectedCategories(preferences.categories.map((c: Category) => c.id));
      setKeywords(preferences.keywords || []);
    } catch (error) {
      void error; // Explicitly mark error as intentionally unused
      toast({
        variant: "destructive",
        title: "错误",
        description: "无法加载订阅偏好，请稍后重试",
      });
    } finally {
      setLoading(false);
    }
  }, [toast]);

  const handleSavePreferences = async () => {
    try {
      await api.put<ApiResponse<UserPreferences>>('/api/v1/preferences', {
        categories: selectedCategories,
        keywords
      });
      toast({
        title: "成功",
        description: "订阅偏好已更新",
      });
    } catch (error) {
      void error; // Explicitly mark error as intentionally unused
      toast({
        variant: "destructive",
        title: "错误",
        description: "更新订阅偏好失败，请重试",
      });
    }
  };

  const handleAddKeyword = () => {
    if (newKeyword && !keywords.includes(newKeyword)) {
      setKeywords([...keywords, newKeyword]);
      setNewKeyword('');
    }
  };

  const handleRemoveKeyword = (keyword: string) => {
    setKeywords(keywords.filter(k => k !== keyword));
  };

  const toggleCategory = (categoryId: number) => {
    setSelectedCategories(prev =>
      prev.includes(categoryId)
        ? prev.filter(id => id !== categoryId)
        : [...prev, categoryId]
    );
  };

  const handleGenerateSummary = async () => {
    try {
      setGenerating(true);
      await api.post<ApiResponse<{ summary: string }>>(
        '/api/v1/subscriptions/user/1/summary'  // TODO: Get actual user ID
      );
      toast({
        title: "成功",
        description: "日报生成成功",
      });
      // TODO: Display summary in a modal or redirect to reports page
    } catch (error) {
      void error; // Explicitly mark error as intentionally unused
      toast({
        variant: "destructive",
        title: "错误",
        description: "生成日报失败，请稍后重试",
      });
    } finally {
      setGenerating(false);
    }
  };

  React.useEffect(() => {
    fetchData();
  }, [fetchData]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader2 className="h-8 w-8 animate-spin" />
        <span className="ml-2">加载中...</span>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>订阅偏好设置</CardTitle>
          <CardDescription>选择您感兴趣的领域和关键词</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-4">
            <Label>领域选择</Label>
            <div className="flex flex-wrap gap-2">
              {categories.map((category) => (
                <Button
                  key={category.id}
                  variant={selectedCategories.includes(category.id) ? "default" : "outline"}
                  onClick={() => toggleCategory(category.id)}
                >
                  {category.name}
                </Button>
              ))}
            </div>
          </div>

          <div className="space-y-4">
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
            <div className="flex flex-wrap gap-2">
              {keywords.map((keyword) => (
                <Badge key={keyword} variant="secondary" className="flex items-center gap-1">
                  {keyword}
                  <X
                    className="h-3 w-3 cursor-pointer"
                    onClick={() => handleRemoveKeyword(keyword)}
                  />
                </Badge>
              ))}
            </div>
          </div>

          <div className="flex justify-between">
            <Button
              variant="outline"
              onClick={handleSavePreferences}
            >
              保存设置
            </Button>
            <Button
              onClick={handleGenerateSummary}
              disabled={generating}
            >
              {generating ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  生成中...
                </>
              ) : (
                '生成今日摘要'
              )}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
